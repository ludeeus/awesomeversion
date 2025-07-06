"""Test for issue #422 - Compound modifier comparison."""

from awesomeversion import AwesomeVersion, AwesomeVersionStrategy


def test() -> None:
    """Test comparing versions with compound modifiers like beta1-dev127513."""
    installed_version = "1.7.0-beta1-dev127513"
    latest_version = "1.7.0-beta2"

    installed_awesome = AwesomeVersion(
        installed_version,
        find_first_match=True,
        ensure_strategy=[AwesomeVersionStrategy.SEMVER],
    )

    latest_awesome = AwesomeVersion(
        latest_version,
        find_first_match=True,
        ensure_strategy=[AwesomeVersionStrategy.SEMVER],
    )

    # Both should be treated as SEMVER
    assert installed_awesome.strategy == AwesomeVersionStrategy.SEMVER
    assert latest_awesome.strategy == AwesomeVersionStrategy.SEMVER

    # Both should extract the correct modifier type
    assert installed_awesome.modifier_type == "beta"
    assert latest_awesome.modifier_type == "beta"

    # Both should have modifiers (not None)
    assert installed_awesome.modifier is not None
    assert latest_awesome.modifier is not None

    # The modifier comparison should work
    assert installed_awesome.modifier < latest_awesome.modifier

    # The main comparison should work (this was the reported issue)
    assert (
        installed_awesome < latest_awesome
    ), f"{installed_awesome} should be less than {latest_awesome}"

    # Test some additional compound modifier scenarios
    dev_version = AwesomeVersion(
        "1.0.0-dev123", ensure_strategy=[AwesomeVersionStrategy.SEMVER]
    )
    alpha_compound = AwesomeVersion(
        "1.0.0-alpha1-build456", ensure_strategy=[AwesomeVersionStrategy.SEMVER]
    )

    assert dev_version.modifier_type == "dev"
    assert alpha_compound.modifier_type == "alpha"

    # dev < alpha according to SEMVER_MODIFIER_MAP
    assert dev_version < alpha_compound
