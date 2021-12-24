"""Special handler for simple."""
from typing import TYPE_CHECKING, Optional

from awesomeversion.strategy import AwesomeVersionStrategy

from .sections import compare_base_sections

if TYPE_CHECKING:
    from awesomeversion import AwesomeVersion


def compare_handler_simple(
    version_a: "AwesomeVersion",
    version_b: "AwesomeVersion",
) -> Optional[bool]:
    """Compare handler simple."""
    if version_a.simple and version_b.simple:
        return compare_base_sections(version_a, version_b)

    if version_a.simple and version_b.strategy not in [
        AwesomeVersionStrategy.SPECIALCONTAINER
    ]:
        if compare_base_sections(version_a, version_b) is None:
            return True

    return None
