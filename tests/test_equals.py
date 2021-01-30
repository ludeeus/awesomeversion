"""Test equals."""
import pytest

from awesomeversion import AwesomeVersion


@pytest.mark.parametrize(
    "version",
    [
        ("1"),
        ("2020.12.1"),
        ("2020"),
        ("2021.2.0b0"),
        ("2021.2.0.dev20210118"),
    ],
)
def test_equals(version):
    """Test equals."""
    version_object = AwesomeVersion(version)
    assert version_object == version
    assert str(version_object) == version
    assert version_object.string == version
    assert version_object == AwesomeVersion(f"v{version}")
    assert version_object == AwesomeVersion(f"v{version}")
