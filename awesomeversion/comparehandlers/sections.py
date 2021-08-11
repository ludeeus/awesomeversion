"""Special handler for sections."""
from typing import TYPE_CHECKING, Optional

from ..utils.regex import RE_MODIFIER, get_regex_match
from .base import CompareHandlerBase

if TYPE_CHECKING:
    from ..awesomeversion import AwesomeVersion


class ComparelHandlerSections(CompareHandlerBase):
    """ComparelHandlerSections class."""

    def handler(self) -> Optional[bool]:
        """Compare handler."""
        base = self._compare_base_sections(self.ver_a, self.ver_b)
        if base is not None:
            return base
        return self._compare_modifier_section(self.ver_a, self.ver_b)

    @staticmethod
    def _compare_base_sections(
        ver_a: "AwesomeVersion", ver_b: "AwesomeVersion"
    ) -> Optional[bool]:
        """Compare base sections between two AwesomeVersion objects."""
        biggest = ver_a.sections if ver_a.sections >= ver_b.sections else ver_b.sections
        for section in range(0, biggest):
            ver_a_section = ver_a.section(section)
            ver_b_section = ver_b.section(section)
            if ver_a_section == ver_b_section:
                continue
            if ver_a_section > ver_b_section:
                return True
            if ver_a_section < ver_b_section:
                return False
        return None

    @staticmethod
    def _compare_modifier_section(
        ver_a: "AwesomeVersion", ver_b: "AwesomeVersion"
    ) -> Optional[bool]:
        """Compare sections between two AwesomeVersion objects."""
        if ver_a.modifier is not None and ver_b.modifier is not None:
            ver_a_modifier = get_regex_match(RE_MODIFIER, ver_a.string.split(".")[-1])
            ver_b_modifier = get_regex_match(RE_MODIFIER, ver_b.string.split(".")[-1])
            if ver_a_modifier and ver_b_modifier:
                if ver_a_modifier.group(3) == ver_b_modifier.group(3):
                    return int(ver_a_modifier.group(4)) > int(ver_b_modifier.group(4))
                return ver_a_modifier.group(3) > ver_b_modifier.group(3)
        return None
