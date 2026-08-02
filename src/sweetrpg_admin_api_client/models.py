from dataclasses import dataclass


@dataclass(frozen=True)
class Banner:
    """A banner message as returned by admin-api's ``GET /banners``. Only the fields
    consumers render are captured - admin-api's model has more (id, scope, timestamps)
    that no known consumer uses yet.
    """

    severity: str
    message: str

    @classmethod
    def from_dict(cls, data: dict) -> "Banner":
        return cls(severity=data["severity"], message=data["message"])


@dataclass(frozen=True)
class MaintenanceMode:
    """A maintenance-mode record as returned by admin-api's
    ``GET /maintenance-modes/active``.
    """

    scope_type: str
    scope_value: str
    label: str
    description: str
    starts_at: str
    ends_at: str | None

    @classmethod
    def from_dict(cls, data: dict) -> "MaintenanceMode":
        return cls(
            scope_type=data["scope_type"],
            scope_value=data["scope_value"],
            label=data["label"],
            description=data["description"],
            starts_at=data["starts_at"],
            ends_at=data.get("ends_at"),
        )
