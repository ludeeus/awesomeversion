"""Special handler for modifier."""
from typing import List, Optional

from awesomeversion.strategy import AwesomeVersionStrategy

from .sections import ComparelHandlerSections

SEMVER_MODIFIER_MAP = {"alpha": 3, "beta": 2, "rc": 1}


class ComparelHandlerSemVerModifier(ComparelHandlerSections):
    """ComparelHandlerSemVerModifier class."""

    @property
    def strategy(self) -> List[AwesomeVersionStrategy]:
        """Return a list of valid strategies for this handler."""
        return [AwesomeVersionStrategy.SEMVER]

    def handler(self) -> Optional[bool]:
        """Compare handler."""
        if self._compare_base_sections(self.ver_a, self.ver_b) is None:
            if (
                self.ver_a.modifier_type is not None
                and self.ver_b.modifier_type is not None
                and self.ver_a.modifier_type != self.ver_b.modifier_type
            ):
                return (
                    SEMVER_MODIFIER_MAP[self.ver_a.modifier_type]
                    > SEMVER_MODIFIER_MAP[self.ver_b.modifier_type]
                )
