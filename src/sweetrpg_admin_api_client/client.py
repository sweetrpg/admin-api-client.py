import logging
import threading
import time
from typing import Optional

import requests
from opentelemetry import propagate

from .models import Banner, MaintenanceMode


__logger = logging.getLogger(__name__)


class _CacheEntry:
    __slots__ = ("fetched_at", "value")

    def __init__(self, value):
        self.fetched_at = time.monotonic()
        self.value = value


class AdminClient:
    """Fetches banner messages and maintenance-mode records from admin-api for a set of
    scopes (e.g. ``["platform", "service:catalog"]``), with a bounded-TTL cache and
    fail-open behavior baked into the client itself - a cross-cutting operational
    contract every consumer must satisfy identically, not a per-app policy choice.
    Every fetch method never raises: a disabled client (no base URL), timeout, network
    error, non-2xx response, or undecodable body all yield an empty list.
    """

    def __init__(
        self,
        base_url: Optional[str],
        ttl_seconds: float = 90,
        timeout_seconds: float = 2,
    ):
        self._base_url = base_url.rstrip("/") if base_url else None
        self._ttl_seconds = ttl_seconds
        self._timeout_seconds = timeout_seconds
        self._lock = threading.Lock()
        self._banner_cache: Optional[_CacheEntry] = None
        self._maintenance_cache: Optional[_CacheEntry] = None

    def fetch_banners(self, scopes: list[str]) -> list[Banner]:
        """Returns active banners for the given scopes, most-severe-first as returned
        by admin-api."""
        cached = self._cached("_banner_cache")
        if cached is not None:
            __logger.debug("banners cache hit")
            return cached
        __logger.debug("banners cache miss, fetching from admin-api")
        banners = self._get_scoped("banners", scopes, Banner.from_dict)
        self._store("_banner_cache", banners)
        return banners

    def fetch_maintenance_modes(self, scopes: list[str]) -> list[MaintenanceMode]:
        """Returns active maintenance-mode records for the given scopes."""
        cached = self._cached("_maintenance_cache")
        if cached is not None:
            __logger.debug("maintenance-modes cache hit")
            return cached
        __logger.debug("maintenance-modes cache miss, fetching from admin-api")
        modes = self._get_scoped(
            "maintenance-modes/active", scopes, MaintenanceMode.from_dict
        )
        self._store("_maintenance_cache", modes)
        return modes

    def _cached(self, attr: str):
        with self._lock:
            entry: Optional[_CacheEntry] = getattr(self, attr)
            if entry is not None and (time.monotonic() - entry.fetched_at) < self._ttl_seconds:
                return entry.value
        return None

    def _store(self, attr: str, value) -> None:
        with self._lock:
            setattr(self, attr, _CacheEntry(value))

    def _get_scoped(self, path: str, scopes: list[str], parse) -> list:
        if not self._base_url:
            __logger.debug("admin-api client disabled, returning empty list for %s", path)
            return []
        try:
            headers = {}
            propagate.inject(headers)
            response = requests.get(
                f"{self._base_url}/{path}",
                params=[("scope", scope) for scope in scopes],
                timeout=self._timeout_seconds,
                headers=headers,
            )
            response.raise_for_status()
            return [parse(item) for item in response.json()]
        except requests.Timeout:
            __logger.warning("timeout fetching %s from admin-api after %f seconds", path, self._timeout_seconds)
            return []
        except requests.RequestException as e:
            __logger.warning("request error fetching %s from admin-api: %s", path, e)
            return []
        except (ValueError, KeyError) as e:
            __logger.warning("parse error in response from admin-api for %s: %s", path, e)
            return []
