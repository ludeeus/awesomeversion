"""Bump version."""
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..awesomeversion import AwesomeVersion


def buildver(version: "AwesomeVersion", **_kwargs: Any) -> str:
    """Bump build version."""
    return str(int(version.string) + 1)


def semver(version: "AwesomeVersion", **kwargs: Any) -> str:
    """Bump semver version."""
    new_version = version.string
    assert version.major
    assert version.minor
    assert version.patch

    if kwargs.get("major"):
        new_version = f"{int(version.major.string) + 1}.0.0"
    elif kwargs.get("minor"):
        new_version = f"{version.major.string}" f".{int(version.minor.string) + 1}" ".0"
    elif kwargs.get("patch"):
        new_version = (
            f"{version.major.string}"
            f".{version.minor.string}"
            f".{int(version.patch.string) +1}"
        )

    return f"{version.prefix}{new_version}" if version.prefix else new_version
