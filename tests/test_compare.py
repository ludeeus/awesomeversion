"""Test compare."""
import pytest

from awesomeversion import AwesomeVersion
from awesomeversion.exceptions import AwesomeVersionCompare


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


@pytest.mark.parametrize(
    "a,compare,b",
    [
        ("2021.2.0", ">", "2021.2.0.dev20210118"),
        ("2021.2.0b0", ">", "2021.2.0.dev20210118"),
        ("2021.2.0", ">", "2021.2.0b0"),
        ("2020.12.1", ">", "2020.12.0"),
        ("2", ">", "1"),
        ("2", ">", 1),
        (2, ">", "1"),
        (2, ">", 1),
        ("2020", ">", "2019"),
        ("1.2.3.4", ">", "1.2.3"),
        ("2020.1", ">", "2020"),
        ("2020.2.0", ">", "2020.1.1."),
        ("1.2.3.4.5.6.7.8.9", ">", "1"),
        ("2020", ">", "2019"),
        ("2020", ">", "2019"),
        ("2020", ">", "2019"),
    ],
)
def test_compare(a, compare, b):
    """Test compare."""
    ver_a = AwesomeVersion(a)
    ver_b = AwesomeVersion(b)
    if compare == ">":
        assert ver_a > ver_b
        assert ver_a > ver_b
        assert ver_a >= ver_b
        assert ver_a != ver_b
        assert ver_a > b
        assert ver_a > b
        assert ver_a >= b
        assert ver_a != b
        assert a > ver_b
        assert a > ver_b
        assert a >= ver_b
        assert a != ver_b
        assert ver_b < ver_a
        assert ver_b <= ver_a
        assert ver_b < a
        assert ver_b <= a

    if str(a).endswith("."):
        a = a[:-1]
    if str(b).endswith("."):
        b = b[:-1]

    assert ver_a.string == str(a)
    assert ver_b.string == str(b)

    assert AwesomeVersion("2019") < AwesomeVersion("2020")
    assert AwesomeVersion("2020.12.0") < AwesomeVersion("2020.12.1")
    assert AwesomeVersion("2020.12.0") > AwesomeVersion("2020.12.dev1602")
    assert AwesomeVersion("2020.12.dev1603") > AwesomeVersion("2020.12.dev1602")
    assert AwesomeVersion("2021.1.0") > AwesomeVersion("2021.1.0b0")
    assert AwesomeVersion("2021.1.0") > AwesomeVersion("2021.1.0b0")
    assert AwesomeVersion("2021.1.0") > AwesomeVersion("2021.1.0b0")
    assert AwesomeVersion("2021.1.0") > AwesomeVersion("2021.1.0b1")
    assert AwesomeVersion("2021.1.0") > AwesomeVersion("2021.1.0dev20210101")
    assert AwesomeVersion("2021.1.0b0") > AwesomeVersion("2021.1.0a0")
    assert AwesomeVersion("2021.1.0b1") > AwesomeVersion("2021.1.0b0")
    assert AwesomeVersion("2021.2.0") > AwesomeVersion("2021.1.0b0")
    assert AwesomeVersion("2021.2.0b0") > AwesomeVersion("2021.1.0")
    assert AwesomeVersion("beta") > AwesomeVersion("stable")
    assert AwesomeVersion("dev") > AwesomeVersion("latest")
    assert AwesomeVersion("latest") > AwesomeVersion("2020.21.1")
    assert AwesomeVersion("latest") > AwesomeVersion("beta")
    assert not AwesomeVersion("0.97.0") > AwesomeVersion("2020.12.1")
    assert not AwesomeVersion("2019") > AwesomeVersion("2020")
    assert not AwesomeVersion("2020.12.dev1602") > AwesomeVersion("2020.12.dev1603")
    assert not AwesomeVersion("2021.1.0b0") > AwesomeVersion("2021.1.0")

    version = AwesomeVersion("2021.2.0b1")
    assert version >= AwesomeVersion("0.112.0")
    assert version == "2021.2.0b1"

    assert AwesomeVersion("1.0.0-alpha0") > AwesomeVersion("1.0.0-beta1")
    assert AwesomeVersion("1.0.0-beta") > AwesomeVersion("1.0.0-beta.1")
    assert AwesomeVersion("1.0.0-beta.2") > AwesomeVersion("1.0.0-beta.1")
    assert AwesomeVersion("1.0.0-alpha0") > AwesomeVersion("1.0.0-rc1")
    assert AwesomeVersion("1.0.0-alpha") > AwesomeVersion("1.0.0-beta")
    assert AwesomeVersion("1.0.0") > AwesomeVersion("1.0.0-beta")
