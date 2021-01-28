"""Test equals."""
from awesomeversion import AwesomeVersion


def test_equals():
    """Test equals."""
    assert AwesomeVersion("2020.12.1") == AwesomeVersion("2020.12.1")
    assert AwesomeVersion("2020") == AwesomeVersion("2020")
    assert AwesomeVersion("2020") == AwesomeVersion("v2020")
    assert AwesomeVersion("2020") == AwesomeVersion("V2020")
    assert AwesomeVersion("2020") != AwesomeVersion("2021")
    assert str(AwesomeVersion("2021.2.0b0")) == "2021.2.0b0"
    assert AwesomeVersion("2021.2.0b0").string == "2021.2.0b0"
    assert str(AwesomeVersion("2021.2.0.dev20210118")) == "2021.2.0.dev20210118"
    assert AwesomeVersion("2021.2.0.dev20210118").string == "2021.2.0.dev20210118"
