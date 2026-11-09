"""Test for issue #549."""

# https://github.com/ludeeus/awesomeversion/issues/549
from awesomeversion import AwesomeVersion

# The precedence chain printed at the end of semver.org §11
SEMVER_SECTION_11_CHAIN = [
    "1.0.0-alpha",
    "1.0.0-alpha.1",
    "1.0.0-alpha.beta",
    "1.0.0-beta",
    "1.0.0-beta.2",
    "1.0.0-beta.11",
    "1.0.0-rc.1",
    "1.0.0",
]


def test_semver_section_11_precedence_chain() -> None:
    """Every link of the semver.org §11 example chain must order correctly."""
    for lower, higher in zip(SEMVER_SECTION_11_CHAIN, SEMVER_SECTION_11_CHAIN[1:]):
        assert AwesomeVersion(lower) < AwesomeVersion(higher), (lower, higher)
        assert AwesomeVersion(higher) > AwesomeVersion(lower), (higher, lower)


def test_semver_prerelease_more_identifiers_win() -> None:
    """A larger set of pre-release fields has a higher precedence."""
    assert AwesomeVersion("1.0.0-alpha") < AwesomeVersion("1.0.0-alpha.1")
    assert AwesomeVersion("1.0.0-alpha.1") < AwesomeVersion("1.0.0-alpha.1.1")
    assert AwesomeVersion("1.0.0-beta") < AwesomeVersion("1.0.0-beta.2")


def test_semver_numeric_identifier_is_lower_than_alphanumeric() -> None:
    """Numeric identifiers have lower precedence than alphanumeric ones."""
    assert AwesomeVersion("1.0.0-alpha.1") < AwesomeVersion("1.0.0-alpha.beta")


def test_sections_still_dominate_the_prerelease() -> None:
    """A newer release section wins over any pre-release of an older one."""
    assert AwesomeVersion("2.0.0-alpha") > AwesomeVersion("1.0.0-beta")
    assert AwesomeVersion("1.0.0") > AwesomeVersion("1.0.0-rc.1")


def test_release_beats_own_prerelease() -> None:
    """A plain version outranks its own pre-releases."""
    assert AwesomeVersion("1.0.0") > AwesomeVersion("1.0.0-beta.11")
