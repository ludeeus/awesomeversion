"""Special handler for sections."""
from __future__ import annotations

from typing import TYPE_CHECKING

from ..const import RE_MODIFIER
from .base import AwesomeVersionCompareHandler

if TYPE_CHECKING:
    from ..awesomeversion import AwesomeVersion


class ComparelHandlerSections(AwesomeVersionCompareHandler):
    """ComparelHandlerSections class."""

    def handler(self) -> bool | None:
        """Compare handler."""
        base = self._compare_base_sections(self.version_a, self.version_b)
        if base is not None:
            return base
        return self._compare_modifier_section(self.version_a, self.version_b)

    @staticmethod
    def _compare_base_sections(
        version_a: "AwesomeVersion", version_b: "AwesomeVersion"
    ) -> bool | None:
        """Compare base sections between two AwesomeVersion objects."""
        biggest = (
            version_a.sections
            if version_a.sections >= version_b.sections
            else version_b.sections
        )
        for section in range(0, biggest):
            version_a_section = version_a.section(section)
            version_b_section = version_b.section(section)
            if version_a_section == version_b_section:
                continue
            if version_a_section > version_b_section:
                return True
            if version_a_section < version_b_section:
                return False

    @staticmethod
    def _compare_modifier_section(
        version_a: "AwesomeVersion", version_b: "AwesomeVersion"
    ) -> bool:
        """Compare sections between two AwesomeVersion objects."""
        if version_a.modifier is not None and version_b.modifier is not None:
            version_a_modifier = RE_MODIFIER.match(version_a.string.split(".")[-1])
            version_b_modifier = RE_MODIFIER.match(version_b.string.split(".")[-1])
            if version_a_modifier.group(3) == version_b_modifier.group(3):
                return int(version_a_modifier.group(4)) > int(
                    version_b_modifier.group(4)
                )
            return version_a_modifier.group(3) > version_b_modifier.group(3)
        return False
