"""Test awesomeversion."""
import json

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
    assert version.prefix is None

    version = AwesomeVersion("v2020.12.1rc0")
    assert version.prefix == "v"

    version2 = AwesomeVersion(version)
    assert version == version2

    assert str(version) == "2020.12.1rc0"
    assert repr(version) == "<AwesomeVersion CalVer '2020.12.1rc0'>"

    with AwesomeVersion("20.12.0") as current:
        with AwesomeVersion("20.12.1") as upstream:
            assert upstream > current


def test_serialization():
    """Test to and from JSON serialization."""
    version = AwesomeVersion("20.12.1")
    dumps = json.dumps({"version": version})
    assert dumps == '{"version": "20.12.1"}'

    assert json.loads(dumps)["version"] == version.string
