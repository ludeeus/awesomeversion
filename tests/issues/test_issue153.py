"""Test for issue #153."""
# https://github.com/ludeeus/awesomeversion/issues/153
from awesomeversion import AwesomeVersion


def test_1():
    """Test for issue #153."""
    dev1 = AwesomeVersion("v1.11.0-dev.1")
    dev2 = AwesomeVersion("v2.0.0-dev.1")
    assert dev1 < dev2


def test() -> None:
    """Test for issue #153."""
    current = AwesomeVersion("v1.10.0")

    dev1 = AwesomeVersion("v1.11.0-dev.1")
    dev2 = AwesomeVersion("v2.0.0-dev.1")
    dev3 = AwesomeVersion("v2.0.0-dev.2")

    assert current < dev1
    assert current < dev2
    assert current < dev3

    assert dev1 > current
    assert dev1 < dev2
    assert dev1 < dev3

    assert dev2 > current
    assert dev2 > dev1
    assert dev2 < dev3

    assert dev3 > current
    assert dev3 > dev1
    assert dev3 > dev2
