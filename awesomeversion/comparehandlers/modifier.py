"""Special handler for modifier."""
from typing import List, Optional

from ..strategy import AwesomeVersionStrategy
from ..utils.regex import (
    RE_MODIFIER,
    RE_SEMVER,
    generate_full_string_regex,
    get_regex_match_group,
)
from .sections import ComparelHandlerSections

SEMVER_MODIFIER_MAP = {"alpha": 1, "beta": 2, "rc": 3}


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

                ver_a_modifier = get_regex_match_group(
                    RE_MODIFIER,
                    get_regex_match_group(
                        generate_full_string_regex(RE_SEMVER), self.ver_a.string, 4
                    ),
                    4,
                )
                ver_b_modifier = get_regex_match_group(
                    RE_MODIFIER,
                    get_regex_match_group(
                        generate_full_string_regex(RE_SEMVER), self.ver_b.string, 4
                    ),
                    4,
                )
                if not ver_a_modifier:
                    return True
                if ver_b_modifier:
                    return int(ver_a_modifier) > int(ver_b_modifier)
        return None
