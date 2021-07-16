"""Special handler for modifier."""
from typing import Optional

from ..const import RE_MODIFIER, AwesomeVersionStrategy
from ..strategies.semver import RE_SEMVER
from .sections import AwesomeVersionCompareHandlerSections

SEMVER_MODIFIER_MAP = {"alpha": 1, "beta": 2, "rc": 3}


class AwesomeVersionCompareHandlerSemVerModifier(AwesomeVersionCompareHandlerSections):
    """AwesomeVersionCompareHandlerSemVerModifier class."""

    @property
    def strategy(self) -> list[AwesomeVersionStrategy]:
        """Return a list of valid strategies for this handler."""
        return [AwesomeVersionStrategy.SEMVER]

    def handler(self) -> Optional[bool]:
        """Compare handler."""
        if self._compare_base_sections(self.version_a, self.version_b) is None:
            if (
                self.version_a.modifier_type is not None
                and self.version_b.modifier_type is not None
            ):
                if self.version_a.modifier_type != self.version_b.modifier_type:
                    return (
                        SEMVER_MODIFIER_MAP[self.version_a.modifier_type]
                        > SEMVER_MODIFIER_MAP[self.version_b.modifier_type]
                    )

                version_a_modifier = RE_MODIFIER.match(
                    RE_SEMVER.match(self.version_a.string).group(4)
                )
                version_b_modifier = RE_MODIFIER.match(
                    RE_SEMVER.match(self.version_b.string).group(4)
                )
                if version_a_modifier and version_b_modifier:
                    if not version_a_modifier.group(4):
                        return True
                    if version_b_modifier.group(4):
                        return int(version_a_modifier.group(4)) > int(
                            version_b_modifier.group(4)
                        )
