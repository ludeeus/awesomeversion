"""Special handler for modifier."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..strategy import VERSION_STRATEGIES_DICT, AwesomeVersionStrategy
from ..utils.regex import (
    RE_MODIFIER,
    extract_digits,
    match_compound_modifier,
    match_modifier_compound_part,
)

SEMVER_MODIFIER_MAP = {"dev": 0, "alpha": 1, "beta": 2, "rc": 3}

if TYPE_CHECKING:
    from awesomeversion import AwesomeVersion


def _extract_modifier_info(version_string: str) -> tuple[str | None, str | None]:
    """Extract modifier number and full modifier string from version."""
    semver_pattern = VERSION_STRATEGIES_DICT[AwesomeVersionStrategy.SEMVER].pattern
    semver_match = semver_pattern.match(version_string)

    if not semver_match or len(semver_match.groups()) < 4:
        return None, None

    full_modifier = semver_match.group(4)
    modifier_match = RE_MODIFIER.match(full_modifier)

    if modifier_match and len(modifier_match.groups()) >= 4:
        modifier_num = modifier_match.group(4)
    else:
        compound_match = match_compound_modifier(full_modifier)
        modifier_num = compound_match.group(2) if compound_match else None

    return modifier_num, full_modifier


def _compare_modifier_types(type_a: str, type_b: str) -> bool:
    """Compare two modifier types using SEMVER_MODIFIER_MAP or alphabetically."""
    priority_a = SEMVER_MODIFIER_MAP.get(type_a)
    priority_b = SEMVER_MODIFIER_MAP.get(type_b)

    if priority_a is not None and priority_b is not None:
        return priority_a > priority_b

    return type_a > type_b


def _compare_compound_parts(part_a: str, part_b: str) -> bool | None:
    """Compare two compound modifier parts. Returns None if equal."""
    mod_match_a = match_modifier_compound_part(part_a)
    mod_match_b = match_modifier_compound_part(part_b)

    if mod_match_a and mod_match_b:
        type_a, num_a = mod_match_a.groups()
        type_b, num_b = mod_match_b.groups()

        if type_a != type_b:
            return _compare_modifier_types(type_a, type_b)

        if num_a and num_b:
            num_val_a, num_val_b = int(num_a), int(num_b)
            if num_val_a != num_val_b:
                return num_val_a > num_val_b

        return None

    nums_a = extract_digits(part_a)
    nums_b = extract_digits(part_b)

    if nums_a and nums_b:
        num_val_a, num_val_b = int(nums_a[0]), int(nums_b[0])
        if num_val_a != num_val_b:
            return num_val_a > num_val_b

    return None


def _compare_compound_modifiers(full_mod_a: str, full_mod_b: str) -> bool | None:
    """Compare compound modifiers after the primary part."""
    parts_a = full_mod_a.split("-")[1:]
    parts_b = full_mod_b.split("-")[1:]

    for part_a, part_b in zip(parts_a, parts_b):
        result = _compare_compound_parts(part_a, part_b)
        if result is not None:
            return result

    return len(parts_a) > len(parts_b) if len(parts_a) != len(parts_b) else None


def compare_handler_semver_modifier(
    version_a: AwesomeVersion,
    version_b: AwesomeVersion,
) -> bool | None:
    """Compare handler sections."""
    if (
        AwesomeVersionStrategy.SEMVER not in (version_a.strategy, version_b.strategy)
        or version_a.modifier_type is None
        or version_b.modifier_type is None
    ):
        return None

    if version_a.modifier_type != version_b.modifier_type:
        mod_a = SEMVER_MODIFIER_MAP.get(version_a.modifier_type)
        mod_b = SEMVER_MODIFIER_MAP.get(version_b.modifier_type)
        if mod_a is not None and mod_b is not None:
            return mod_a > mod_b

    mod_num_a, full_mod_a = _extract_modifier_info(version_a.string)
    mod_num_b, full_mod_b = _extract_modifier_info(version_b.string)

    result = None
    if mod_num_a and mod_num_b:
        primary_diff = int(mod_num_a) - int(mod_num_b)
        if primary_diff != 0:
            result = primary_diff > 0
    elif mod_num_a and not mod_num_b:
        result = False
    elif not mod_num_a and mod_num_b:
        result = True

    if result is None and full_mod_a and full_mod_b:
        compound_result = _compare_compound_modifiers(full_mod_a, full_mod_b)
        if compound_result is not None:
            result = compound_result

    return result if result is not None else False
