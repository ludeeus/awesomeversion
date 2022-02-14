"""Basic test to execute in CI."""
from awesomeversion import AwesomeVersion


def test_awesomeversion() -> None:
    """Basic test functionalify."""
    version = AwesomeVersion("1.2.3")
    assert version == "1.2.3"
    assert not version.dev


if __name__ == "__main__":
    print("Running basic test")
    test_awesomeversion()
    print("Basic test completed")
