"""Test for issue #26."""
# https://github.com/ludeeus/awesomeversion/issues/26
from awesomeversion import AwesomeVersion


def test():
    """Test for issue #26."""
    current = AwesomeVersion(" 123")
    upstream = AwesomeVersion("123")
    assert current == upstream
