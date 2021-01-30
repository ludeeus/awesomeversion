"""Test compare."""
import pytest

from awesomeversion import AwesomeVersion
from awesomeversion.exceptions import AwesomeVersionCompare


@pytest.mark.parametrize(
    "version_a,version_b",
    [
        ("2021.2.0", "2021.2.0.dev20210118"),
        ("2021.2.0b0", "2021.2.0.dev20210118"),
        ("2021.2.0", "2021.2.0b0"),
        ("2020.12.1", "2020.12.0"),
        ("2", "1"),
        ("2", 1),
        (2, "1"),
        (2, 1),
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
        ("2021.2.0", "2021.1.0b0"),
        ("2021.2.0b0", "2021.1.0"),
        ("beta", "stable"),
        ("dev", "latest"),
        ("latest", "2020.21.1"),
        ("latest", "beta"),
        ("1.0.0-alpha0", "1.0.0-beta1"),
        ("1.0.0-beta", "1.0.0-beta.1"),
        ("1.0.0-beta.2", "1.0.0-beta.1"),
        ("1.0.0-alpha0", "1.0.0-rc1"),
        ("1.0.0-alpha", "1.0.0-beta"),
        ("1.0.0", "1.0.0-beta"),
        ("2020", "2019"),
        ("2020", "2019"),
        ("2020", "2019"),
        ("2020", "2019"),
    ],
)
def test_compare(version_a, version_b):
    """Test compare."""
    ver_a = AwesomeVersion(version_a)
    ver_b = AwesomeVersion(version_b)

    assert ver_a > ver_b
    assert ver_a > ver_b
    assert ver_a >= ver_b
    assert ver_a != ver_b
    assert ver_a > version_b
    assert ver_a > version_b
    assert ver_a >= version_b
    assert ver_a != version_b
    assert version_a > ver_b
    assert version_a > ver_b
    assert version_a >= ver_b
    assert version_a != ver_b
    assert ver_b < ver_a
    assert ver_b <= ver_a
    assert ver_b < version_a
    assert ver_b <= version_a

    if str(version_a).endswith("."):
        version_a = version_a[:-1]
    if str(version_b).endswith("."):
        version_b = version_b[:-1]

    assert ver_a.string == str(version_a)
    assert ver_b.string == str(version_b)


def test_invalid_compare():
    """Test invalid compare."""
    invalid = None
    with pytest.raises(
        AwesomeVersionCompare, match="Not a valid AwesomeVersion object"
    ):
        assert AwesomeVersion("2020.12.1") > invalid

    with pytest.raises(
        AwesomeVersionCompare, match="Not a valid AwesomeVersion object"
    ):
        assert AwesomeVersion("2020.12.1") < invalid

    with pytest.raises(
        AwesomeVersionCompare, match="Not a valid AwesomeVersion object"
    ):
        assert AwesomeVersion("2020.12.1") == invalid

    with pytest.raises(AwesomeVersionCompare, match="Can't compare unknown"):
        assert AwesomeVersion("2020.12.1") > AwesomeVersion("string")

    with pytest.raises(AwesomeVersionCompare, match="Can't compare unknown"):
        assert AwesomeVersion("2020.12.1") < AwesomeVersion("string")