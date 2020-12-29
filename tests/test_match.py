"""Test match."""
from awesomeversion.match import version_strategy
from awesomeversion.strategy import AwesomeVersionStrategy


def test_buildver():
    """Test buildver."""
    assert version_strategy("123") == AwesomeVersionStrategy.BUILDVER
    assert version_strategy("123.123") != AwesomeVersionStrategy.BUILDVER


def test_calver():
    """Test calver."""
    assert version_strategy("20.1.0") == AwesomeVersionStrategy.CALVER
    assert version_strategy("0.118.0") != AwesomeVersionStrategy.CALVER


def test_semver():
    """Test semver."""
    assert version_strategy("0.118.0") == AwesomeVersionStrategy.SEMVER
    assert version_strategy("20.1.0") != AwesomeVersionStrategy.SEMVER


def test_simplever():
    """Test simplever."""
    assert version_strategy("1.2.3.4.5") == AwesomeVersionStrategy.SIMPLEVER
    assert version_strategy("20.1.0") != AwesomeVersionStrategy.SIMPLEVER


def test_unknown():
    """Test unknown."""
    assert version_strategy("string") == AwesomeVersionStrategy.UNKNOWN
    assert version_strategy("20.1.0") != AwesomeVersionStrategy.UNKNOWN


def test_specialcontainer():
    """Test specialcontainer."""
    assert version_strategy("latest") == AwesomeVersionStrategy.SPECIALCONTAINER
    assert version_strategy("stable") == AwesomeVersionStrategy.SPECIALCONTAINER
    assert version_strategy("beta") == AwesomeVersionStrategy.SPECIALCONTAINER
    assert version_strategy("dev") == AwesomeVersionStrategy.SPECIALCONTAINER
    assert version_strategy("20.1.0") != AwesomeVersionStrategy.SPECIALCONTAINER