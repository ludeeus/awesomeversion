"""Special handler for simple."""
from typing import TYPE_CHECKING, Optional
from .sections import compare_base_sections

from awesomeversion.strategy import AwesomeVersionStrategy


if TYPE_CHECKING:
    from awesomeversion import AwesomeVersion


def compare_handler_simple(
    version_a: "AwesomeVersion",
    version_b: "AwesomeVersion",
) -> Optional[bool]:
    """Compare handler simple."""
    if version_a.simple and version_b.simple:
        if compare_base_sections(version_a, version_b) is None:
            return False

    if version_a.simple and version_b.strategy not in [
        AwesomeVersionStrategy.SPECIALCONTAINER
    ]:
        if compare_base_sections(version_a, version_b) is None:
            return True

    return None
