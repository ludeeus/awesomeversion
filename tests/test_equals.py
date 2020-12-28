"""Test equals."""
from awesomeversion import AwesomeVersion


def test_equals():
    """Test equals."""
    assert AwesomeVersion("2020.12.1") == AwesomeVersion("2020.12.1")
    assert AwesomeVersion("2020") == AwesomeVersion("2020")
    assert AwesomeVersion("2020") == AwesomeVersion("v2020")
    assert AwesomeVersion("2020") == AwesomeVersion("V2020")
    assert AwesomeVersion("2020") != AwesomeVersion("2021")
