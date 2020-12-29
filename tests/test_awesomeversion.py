"""Test awesomeversion."""
from awesomeversion import AwesomeVersion


def test_awesomeversion():
    """Test awesomeversion."""
    version = AwesomeVersion("2020.12.1")
    assert not version.beta

    version = AwesomeVersion("2020.12.1a0")
    assert version.alpha

    version = AwesomeVersion("2020.12.1b0")
    assert version.beta

    version = AwesomeVersion("2020.12.1dev0")
    assert version.dev

    version = AwesomeVersion("2020.12.1d0")
    assert version.dev

    version = AwesomeVersion("2020.12.1rc0")
    assert version.release_candidate

    version = AwesomeVersion("v2020.12.1rc0")
    version2 = AwesomeVersion(version)
    assert version == version2

    assert str(version) == "2020.12.1rc0"
    assert repr(version) == "<AwesomeVersion CalVer '2020.12.1rc0'>"
