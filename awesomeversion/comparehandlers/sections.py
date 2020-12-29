"""Special handler for sections."""
from typing import TYPE_CHECKING

from ..match import RE_DIGIT, RE_MODIFIER
from .base import CompareHandlerBase

if TYPE_CHECKING:
    from ..awesomeversion import AwesomeVersion


class ComparelHandlerSections(CompareHandlerBase):
    def handler(self) -> bool:
        """Compare handler."""
        return self._compare_sections(self.ver_a, self.ver_b)

    @staticmethod
    def _compare_sections(ver_a: "AwesomeVersion", ver_b: "AwesomeVersion") -> bool:
        """Compare sections between two AwesomeVersion objects."""
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
        if ver_a.modifier and ver_b.modifier:
            ver_a_modifier = RE_MODIFIER.match(ver_a.string.split(".")[-1])
            ver_b_modifier = RE_MODIFIER.match(ver_b.string.split(".")[-1])
            ver_a_modifier_value = RE_DIGIT.match(ver_a_modifier.group(1)).group(1)
            ver_b_modifier_value = RE_DIGIT.match(ver_b_modifier.group(1)).group(1)
            if ver_a_modifier.group(2) == ver_b_modifier.group(2):
                return ver_a_modifier_value > ver_b_modifier_value
            return ver_a_modifier.group(2) > ver_b_modifier.group(2)
        return False
