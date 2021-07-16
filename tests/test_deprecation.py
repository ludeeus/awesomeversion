"""Test deprecations."""
from awesomeversion import AwesomeVersion, AwesomeVersionStrategy


def test_import_awesomeversion_strategy(caplog):
    """Test import strategy."""
    from awesomeversion.strategy import AwesomeVersionStrategy

    assert (
        "Importing AwesomeVersionStrategy from awesomeversion.strategy is deprecated, "
        "import it from awesomeversion instead" in caplog.text
    )


def test_ensure_strategy(caplog):
    """Test ensure_strategy."""
    AwesomeVersion.ensure_strategy("1.2.3", [AwesomeVersionStrategy.SEMVER])
    assert (
        "Using AwesomeVersion.ensure_strategy(version, strategy) is deprecated, "
        "use AwesomeVersion(version, strategy) instead" in caplog.text
    )
