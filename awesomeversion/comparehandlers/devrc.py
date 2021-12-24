"""Special handler for dev."""
from typing import TYPE_CHECKING, Optional

from .sections import compare_base_sections

if TYPE_CHECKING:
    from awesomeversion import AwesomeVersion


def compare_handler_devrc(
    version_a: "AwesomeVersion",
    version_b: "AwesomeVersion",
) -> Optional[bool]:
    """Compare handler devrc."""
    a_last = version_a.string.split(".")[-1]
    b_last = version_b.string.split(".")[-1]
    if (not a_last.startswith("dev") and b_last.startswith("dev")) or (
        not a_last.startswith("rc") and b_last.startswith("rc")
    ):
        version_b._version = (  # pylint: disable=protected-access
            version_b.string.replace(f".{b_last}", "")
        )
        if version_a.string == version_b.string:
            return True
        if compare_base_sections(version_a, version_b) is None:
            return True
    return None
