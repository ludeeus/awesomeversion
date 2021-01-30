"""Test test_version_scheme."""
import pytest

from awesomeversion import AwesomeVersion
from awesomeversion.strategy import AwesomeVersionStrategy


@pytest.mark.parametrize(
    "version,strategy,dev,beta,modifier,modifier_type",
    [
        ("0.118.0", AwesomeVersionStrategy.SEMVER, False, False, None, None),
        ("1.0.0b1", AwesomeVersionStrategy.PEP440, False, True, "b1", "b"),
        ("1.0.0-beta.1", AwesomeVersionStrategy.SEMVER, False, True, "beta.1", "beta"),
        ("v1.0.0-beta.1", AwesomeVersionStrategy.SEMVER, False, True, "beta.1", "beta"),
        ("2021.2.0.dev1", AwesomeVersionStrategy.CALVER, True, False, "dev1", "dev"),
        ("stable", AwesomeVersionStrategy.SPECIALCONTAINER, False, False, None, None),
    ],
)
def test_version_scheme(version, strategy, dev, beta, modifier, modifier_type):
    """Test that the version matches the expected scheme."""
    version_object = AwesomeVersion(version)
    assert str(version_object) == version
    assert version_object.strategy == strategy
    assert version_object.dev == dev
    assert version_object.beta == beta
    assert version_object.modifier == modifier
    assert version_object.modifier_type == modifier_type
