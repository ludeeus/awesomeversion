"""Test for issue #14."""

# https://github.com/ludeeus/awesomeversion/issues/333
from awesomeversion import AwesomeVersion
from awesomeversion.strategy import AwesomeVersionStrategy


def test() -> None:
    """Test for issue #333."""
    version = AwesomeVersion("v3.4-rc5") 
    assert version < "v3.6-rc2"
    assert version.release_candidate
    assert version.strategy != AwesomeVersionStrategy.UNKNOWN
