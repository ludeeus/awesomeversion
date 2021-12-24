"""Special handler for sections."""
from typing import TYPE_CHECKING, Optional

from ..utils.regex import RE_MODIFIER

if TYPE_CHECKING:
    from ..awesomeversion import AwesomeVersion


def compare_handler_sections(
    version_a: "AwesomeVersion",
    version_b: "AwesomeVersion",
) -> Optional[bool]:
    """Compare handler sections."""
    base = compare_base_sections(version_a, version_b)
    if base is not None:
        return base
    return compare_modifier_section(version_a, version_b)


def compare_base_sections(
    version_a: "AwesomeVersion",
    version_b: "AwesomeVersion",
) -> Optional[bool]:
    """Compare base sections between two AwesomeVersion objects."""
    biggest = (
        version_a.sections
        if version_a.sections >= version_b.sections
        else version_b.sections
    )
    for section in range(0, biggest):
        ver_a_section = version_a.section(section)
        ver_b_section = version_b.section(section)
        if ver_a_section == ver_b_section:
            continue
        if ver_a_section > ver_b_section:
            return True
        if ver_a_section < ver_b_section:
            return False
    return None


def compare_modifier_section(
    version_a: "AwesomeVersion",
    version_b: "AwesomeVersion",
) -> Optional[bool]:
    """Compare sections between two AwesomeVersion objects."""
    if version_a.modifier is not None and version_b.modifier is not None:
        version_a_modifier = RE_MODIFIER.match(version_a.string.split(".")[-1])
        version_b_modifier = RE_MODIFIER.match(version_b.string.split(".")[-1])
        if version_a_modifier and version_b_modifier:
            if version_a_modifier.group(3) == version_b_modifier.group(3):
                return int(version_a_modifier.group(4)) > int(
                    version_b_modifier.group(4)
                )
            return version_a_modifier.group(3) > version_b_modifier.group(3)
    return None
