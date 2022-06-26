"""Test compare."""
import pytest

from awesomeversion import AwesomeVersion
from awesomeversion.exceptions import AwesomeVersionCompareException
from awesomeversion.typing import VersionType


@pytest.mark.parametrize(
    "version_a,version_b",
    [
        ("1.0.0-beta.10", "1.0.0-beta.9"),
        ("1.0.0-alpha10", "1.0.0-alpha9"),
        ("2021.2.0", "2021.2.0.dev20210118"),
        ("2021.2.0b0", "2021.2.0.dev20210118"),
        ("2021.2.0", "2021.2.0b0"),
        ("2020.12.1", "2020.12.0"),
        ("2", "1"),
        ("2", 1),
        (2, "1"),
        (2, 1),
        ("5.11", "5.10"),
        ("1.1", "1.0"),
        ("2020", "2019"),
        ("1.2.3.4", "1.2.3"),
        ("2020.1", "2020"),
        ("2020.2.0", "2020.1.1."),
        ("1.2.3.4.5.6.7.8.9", "1"),
        ("2020.12.0", "2020.12.dev1602"),
        ("2020.12.dev1603", "2020.12.dev1602"),
        ("2021.1.0", "2021.1.0b0"),
        ("2021.1.0", "2021.1.0b0"),
        ("2021.1.0", "2021.1.0b1"),
        ("2021.1.0", "2021.1.0dev20210101"),
        ("2021.1.0b0", "2021.1.0a0"),
        ("2021.1.0b1", "2021.1.0b0"),
        ("2021.1.0b1", "2021.1.0dev0"),
        ("2021.1.0b1", "2021.1.0.dev0"),
        ("2021.1.0", "2021.1.0.dev0"),
        ("2021.2.0", "2021.1.0b0"),
        ("2021.2.0b0", "2021.1.0"),
        ("2021.2.0b10", "2021.1.0b2"),
        ("beta", "stable"),
        ("dev", "latest"),
        ("latest", "2020.21.1"),
        ("latest", "beta"),
        ("1.0.0-beta0", "1.0.0-alpha1"),
        ("1.0.0-beta", "1.0.0-beta.1"),
        ("1.0.0-beta1", "1.0.0-beta"),
        ("1.0.0-beta.2", "1.0.0-beta.1"),
        ("1.0.0-rc0", "1.0.0-alpha1"),
        ("1.0.0-beta", "1.0.0-alpha"),
        ("1.0.0", "1.0.0-beta1"),
        ("1.0.0", "1.0.0-beta"),
        ("6.0.rc1", "6.0.dev20210429"),
        ("6.0", "6.0.rc1"),
        ("1.2.3.4.5.6.7.8", "1.2.3.4.5.6.6.8"),
        ("1.0.0b1", "1.0.0b0"),
        ("1.0.0b10", "1.0.0b9"),
        ("1.0.0", "1.0.0b0"),
        (1.0, "1.0.0rc0"),
    ],
)
def test_compare(version_a: VersionType, version_b: VersionType) -> None:
    """Test compare."""
    ver_a = AwesomeVersion(version_a)
    ver_b = AwesomeVersion(version_b)

    assert ver_a > ver_b
    assert ver_a >= ver_b
    assert ver_a != ver_b
    assert ver_a > version_b
    assert ver_a >= version_b
    assert ver_a != version_b
    assert version_a > ver_b
    assert version_a >= ver_b
    assert version_a != ver_b
    assert ver_b < ver_a
    assert ver_b <= ver_a
    assert ver_b < version_a
    assert ver_b <= version_a

    if str(version_a).endswith("."):
        version_a = str(version_a)[:-1]
    if str(version_b).endswith("."):
        version_b = str(version_b)[:-1]

    assert ver_a.string == str(version_a)
    assert ver_b.string == str(version_b)


def test_invalid_compare() -> None:
    """Test invalid compare."""
    invalid = None
    with pytest.raises(
        AwesomeVersionCompareException, match="Not a valid AwesomeVersion object"
    ):
        assert AwesomeVersion("2020.12.1") > invalid

    with pytest.raises(
        AwesomeVersionCompareException, match="Not a valid AwesomeVersion object"
    ):
        assert AwesomeVersion("2020.12.1") < invalid

    with pytest.raises(
        AwesomeVersionCompareException, match="Not a valid AwesomeVersion object"
    ):
        assert AwesomeVersion("2020.12.1") == invalid

    with pytest.raises(
        AwesomeVersionCompareException,
        match="Can't compare <CalVer 2020.12.1> and <unknown string>",
    ):
        assert AwesomeVersion("2020.12.1") > AwesomeVersion("string")

    with pytest.raises(
        AwesomeVersionCompareException,
        match="Can't compare <CalVer 2020.12.1> and <unknown >",
    ):
        assert AwesomeVersion("2020.12.1") < AwesomeVersion("")

    with pytest.raises(
        AwesomeVersionCompareException,
        match="Can't compare <CalVer 2020.12.1> and <unknown None>",
    ):
        assert AwesomeVersion("2020.12.1") < AwesomeVersion(None)


@pytest.mark.parametrize(
    "version",
    [1, "1", 1.0, "1.0", 5.10, "5.10"],
)
def test_falsy_compare(version: VersionType) -> None:
    """Test compare."""
    ver_a = AwesomeVersion(version)
    ver_b = AwesomeVersion(version)

    assert ver_a == ver_b
    assert ver_a <= ver_b
    assert ver_a >= ver_b

    assert not version != ver_b
    assert not version > ver_b
    assert not version < ver_b

    assert not ver_a != version
    assert not ver_a > version
    assert not ver_a < version
