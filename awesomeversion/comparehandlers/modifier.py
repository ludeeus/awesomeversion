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


def _semver_prerelease_atoms(version_string: str) -> list[str] | None:
    """Return the comparison atoms of a SemVer pre-release.

    The pre-release is split on '.' and on '-', the way the compound
    modifier comparison splits its parts, so that 'alpha.1' and 'alpha-dev1'
    both yield their individual pieces to compare pairwise.
    """
    semver_pattern = VERSION_STRATEGIES_DICT[AwesomeVersionStrategy.SEMVER].pattern
    semver_match = semver_pattern.match(version_string)

    if not semver_match or len(semver_match.groups()) < 4 or not semver_match.group(4):
        return None

    atoms: list[str] = []
    for identifier in semver_match.group(4).split("."):
        atoms.extend(identifier.split("-"))
    return atoms


def _compare_prerelease_atom(atom_a: str, atom_b: str) -> bool | None:
    """Compare two pre-release atoms. Returns None if equal."""
    if atom_a == atom_b:
        return None

    numeric_a = atom_a.isdigit()
    numeric_b = atom_b.isdigit()
    if numeric_a and numeric_b:
        num_val_a, num_val_b = int(atom_a), int(atom_b)
        return num_val_a > num_val_b if num_val_a != num_val_b else None
    if numeric_a:
        return False
    if numeric_b:
        return True

    mod_match_a = match_modifier_compound_part(atom_a)
    mod_match_b = match_modifier_compound_part(atom_b)
    if mod_match_a and mod_match_b:
        type_a, num_a = mod_match_a.groups()
        type_b, num_b = mod_match_b.groups()
        if type_a != type_b:
            return _compare_modifier_types(type_a, type_b)
        num_val_a = int(num_a) if num_a else None
        num_val_b = int(num_b) if num_b else None
        if num_val_a is not None and num_val_b is not None:
            return num_val_a > num_val_b if num_val_a != num_val_b else None
        if num_val_a is not None:
            return True
        if num_val_b is not None:
            return False
        return None

    return atom_a > atom_b


def _compare_semver_prerelease(version_a: str, version_b: str) -> bool | None:
    """Compare two SemVer pre-releases per the precedence rules of §11.

    The pre-release pieces are compared pairwise; numeric pieces compare
    numerically and have lower precedence than alphanumeric ones, a larger
    set of pre-release pieces has higher precedence than a smaller set, and
    the established modifier ordering (dev < alpha < beta < rc) applies to
    the alphabetic part of each piece.  Returns None when the pre-releases
    are equal (or missing), so the caller can fall through.
    """
    atoms_a = _semver_prerelease_atoms(version_a)
    atoms_b = _semver_prerelease_atoms(version_b)
    if atoms_a is None or atoms_b is None:
        return None

    for atom_a, atom_b in zip(atoms_a, atoms_b):
        result = _compare_prerelease_atom(atom_a, atom_b)
        if result is not None:
            return result

    if len(atoms_a) != len(atoms_b):
        return len(atoms_a) > len(atoms_b)
    return None


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
        version_a.strategy == AwesomeVersionStrategy.SEMVER
        and version_b.strategy == AwesomeVersionStrategy.SEMVER
    ):
        # Both sides are SemVer: the pre-release identifiers decide the
        # ordering, per semver.org §11.
        semver_result = _compare_semver_prerelease(version_a.string, version_b.string)
        if semver_result is not None:
            return semver_result

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
