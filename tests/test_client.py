from sweetrpg_admin_api_client import AdminClient


def test_disabled_client_returns_no_banners_without_making_a_request():
    client = AdminClient(base_url=None)
    assert client.fetch_banners(["platform"]) == []


def test_disabled_client_returns_no_maintenance_modes_without_making_a_request():
    client = AdminClient(base_url=None)
    assert client.fetch_maintenance_modes(["platform"]) == []


def test_unreachable_admin_api_fails_open_for_banners():
    # Port 1 is a reserved/unassigned port that refuses connections immediately on any
    # platform this runs on - exercises the network-error branch without a mock server
    # or a real timeout wait.
    client = AdminClient(base_url="http://127.0.0.1:1")
    assert client.fetch_banners(["platform"]) == []


def test_unreachable_admin_api_fails_open_for_maintenance_modes():
    client = AdminClient(base_url="http://127.0.0.1:1")
    assert client.fetch_maintenance_modes(["platform"]) == []


def test_maintenance_mode_from_dict_captures_scope_and_dates():
    from sweetrpg_admin_api_client import MaintenanceMode

    mode = MaintenanceMode.from_dict(
        {
            "scope_type": "service",
            "scope_value": "catalog",
            "label": "Scheduled downtime",
            "description": "Upgrading the database.",
            "starts_at": "2026-08-01T00:00:00Z",
            "ends_at": "2026-08-01T04:00:00Z",
        }
    )
    assert mode.scope_type == "service"
    assert mode.scope_value == "catalog"
    assert mode.ends_at == "2026-08-01T04:00:00Z"


def test_maintenance_mode_from_dict_ends_at_optional():
    from sweetrpg_admin_api_client import MaintenanceMode

    mode = MaintenanceMode.from_dict(
        {
            "scope_type": "platform",
            "scope_value": "",
            "label": "Platform maintenance",
            "description": "Full outage.",
            "starts_at": "2026-08-01T00:00:00Z",
        }
    )
    assert mode.ends_at is None
