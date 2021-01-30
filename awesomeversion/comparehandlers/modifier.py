"""Special handler for modifier."""
from typing import List, Optional

from ..match import RE_MODIFIER, RE_SEMVER
from ..strategy import AwesomeVersionStrategy
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
            ):
                if self.ver_a.modifier_type != self.ver_b.modifier_type:
                    return (
                        SEMVER_MODIFIER_MAP[self.ver_a.modifier_type]
                        > SEMVER_MODIFIER_MAP[self.ver_b.modifier_type]
                    )

                ver_a_modifier = RE_MODIFIER.match(
                    RE_SEMVER.match(self.ver_a.string).group(4)
                )
                ver_b_modifier = RE_MODIFIER.match(
                    RE_SEMVER.match(self.ver_b.string).group(4)
                )
                if ver_a_modifier and ver_b_modifier:
                    if not ver_a_modifier.group(4):
                        return True
                    if ver_b_modifier.group(4):
                        return ver_a_modifier.group(4) > ver_b_modifier.group(4)
