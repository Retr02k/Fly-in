from fly_in.header.header import ZoneType


def test_zone_type_accepts_normal_string() -> None:
    assert ZoneType("normal") == ZoneType.NORMAL


def test_zone_type_has_expected_members() -> None:
    # adjust these to whatever ZoneType actually defines
    assert hasattr(ZoneType, "NORMAL")
