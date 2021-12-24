"""Special handler for modifier."""
from typing import TYPE_CHECKING, Optional

from ..strategy import AwesomeVersionStrategy
from ..utils.regex import (
    RE_MODIFIER,
    RE_SEMVER,
    generate_full_string_regex,
    get_regex_match_group,
)

SEMVER_MODIFIER_MAP = {"alpha": 1, "beta": 2, "rc": 3}

if TYPE_CHECKING:
    from awesomeversion import AwesomeVersion


def compare_handler_semver_modifier(
    version_a: "AwesomeVersion",
    version_b: "AwesomeVersion",
) -> Optional[bool]:
    """Compare handler sections."""
    if (
        AwesomeVersionStrategy.SEMVER
        not in (
            version_a.strategy,
            version_b.strategy,
        )
        or (version_a.modifier_type is None or version_b.modifier_type is None)
    ):
        return None

    if version_a.modifier_type != version_b.modifier_type:
        return (
            SEMVER_MODIFIER_MAP[version_a.modifier_type]
            > SEMVER_MODIFIER_MAP[version_b.modifier_type]
        )

    ver_a_modifier = get_regex_match_group(
        RE_MODIFIER,
        get_regex_match_group(
            generate_full_string_regex(RE_SEMVER), version_a.string, 4
        ),
        4,
    )
    ver_b_modifier = get_regex_match_group(
        RE_MODIFIER,
        get_regex_match_group(
            generate_full_string_regex(RE_SEMVER), version_b.string, 4
        ),
        4,
    )
    if not ver_a_modifier:
        return True
    if ver_b_modifier:
        return int(ver_a_modifier) > int(ver_b_modifier)
