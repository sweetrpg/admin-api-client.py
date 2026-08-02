# admin-api-client.py

[![Coverage](https://img.shields.io/endpoint?url=https://sweetrpg.github.io/admin-api-client.py/coverage-badge.json)](https://sweetrpg.github.io/admin-api-client.py/)

Python client SDK for `admin-api`: fetches active banner messages and maintenance-mode records.

## Scope

`AdminClient` exposes two methods, `fetch_banners(scopes)` and
`fetch_maintenance_modes(scopes)`. Unlike a domain API client SDK, caching, request timeout
(2s), and fail-open behavior are baked into this package rather than left to the consumer -
every frontend must behave identically for this cross-cutting concern. Both methods cache their
own result for 90 seconds and never raise: a disabled client (no base URL), timeout, network
error, non-2xx response, or undecodable body all yield an empty list.

## Usage

```python
import os
from sweetrpg_admin_api_client import AdminClient

client = AdminClient(base_url=os.environ.get("ADMIN_API_URL"))
banners = client.fetch_banners(["platform", "service:catalog"])
maintenance_modes = client.fetch_maintenance_modes(["platform", "service:catalog"])
```
