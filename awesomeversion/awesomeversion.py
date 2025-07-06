"""AwesomeVersion."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Any, Dict
from warnings import warn

from .comparehandlers.container import compare_handler_container
from .comparehandlers.modifier import compare_handler_semver_modifier
from .comparehandlers.sections import compare_handler_sections
from .comparehandlers.simple import compare_handler_simple
from .exceptions import AwesomeVersionCompareException, AwesomeVersionStrategyException
from .strategy import (
    MAJOR_STRATEGIES,
    VERSION_STRATEGIES,
    VERSION_STRATEGIES_DICT,
    VERSIONED_STRATEGIES,
    AwesomeVersionStrategy,
    AwesomeVersionStrategyDescription,
)
from .utils.regex import (
    RE_DIGIT,
    RE_MODIFIER,
    RE_SIMPLE,
    compile_regex,
    generate_full_string_regex,
    match_compound_modifier,
)

if TYPE_CHECKING:
    from .typing import EnsureStrategyIterableType, EnsureStrategyType, VersionType


class AwesomeVersion(str):
    """
    AwesomeVersion class.
    """

    _version: str = ""
    _modifier: str | None = None
    _modifier_type: str | None = None
    _sections: int | None = None
    _ensure_strategy: EnsureStrategyIterableType = []

    def __init__(
        self,  # pylint: disable=unused-argument
        version: VersionType,
        *,
        ensure_strategy: EnsureStrategyType = None,
        find_first_match: bool = False,
        **kwargs: Any,
    ) -> None:
        """
        Initialize AwesomeVersion.

        **args**:

        version:
            The version to create a AwesomeVersion object from

        **kwargs**:

        ensure_strategy:
            Match the AwesomeVersion object against spesific
            strategies when creating if. If it does not match
            AwesomeVersionStrategyException will be raised

        find_first_match:
            If True, the version given will be scanned for the first
            match of the given ensure_strategy. Raises
            AwesomeVersionStrategyException If it is not found
            for any of the given strategies.
        """
        if isinstance(version, AwesomeVersion):
            self._version = version._version
        else:
            version_str = str(version)
            self._version = version_str.strip() if version_str else ""

        if find_first_match and not ensure_strategy:
            warn(
                "Can not use find_first_match without ensure_strategy, "
                "this is ignored and will start raising an exception in 2025.",
                stacklevel=2,
            )

        if ensure_strategy is not None:
            self._ensure_strategy = ensure_strategy = (
                ensure_strategy
                if isinstance(ensure_strategy, (list, tuple))
                else [ensure_strategy]
            )
            if AwesomeVersionStrategy.UNKNOWN in ensure_strategy:
                raise AwesomeVersionStrategyException(
                    f"Can't use {AwesomeVersionStrategy.UNKNOWN.value} as ensure_strategy"
                )
            if find_first_match:
                for strategy in self._ensure_strategy or []:
                    description = VERSION_STRATEGIES_DICT[strategy]
                    match = compile_regex(description.regex_string).search(
                        self._version
                    )
                    if match is not None:
                        self._version = match.group(0)
                        break

            if self.strategy not in ensure_strategy:
                raise AwesomeVersionStrategyException(
                    f"Strategy {self.strategy.value} does not match "
                    f"{[strategy.value for strategy in ensure_strategy]} for {version}"
                )

        if self._version and self._version[-1] == ".":
            self._version = self._version[:-1]

        str.__init__(self._version)

    def __new__(
        cls,
        version: str,
        *_: Any,
        **__: Any,
    ) -> AwesomeVersion:
        """Create a new AwesomeVersion object."""

        return super().__new__(cls, version)

    def __enter__(self) -> AwesomeVersion:
        return self

    def __exit__(self, *_: Any, **__: Any) -> None:
        pass

    def __repr__(self) -> str:
        return f"<AwesomeVersion {self.strategy.value} '{self.string}'>"

    def __str__(self) -> str:
        return str(self._version)

    def __eq__(self, compareto: VersionType) -> bool:
        """Check if equals to."""
        compareto = self._ensure_awesome_version(compareto)
        return self.string == compareto.string

    def __lt__(self, compareto: VersionType) -> bool:
        """Check if less than."""
        compareto = self._ensure_awesome_version(compareto)

        if self.string == compareto.string:
            return False

        self._validate_comparison_strategy(compareto)
        return self._compare_versions(compareto, self)

    def __gt__(self, compareto: VersionType) -> bool:
        """Check if greater than."""
        compareto = self._ensure_awesome_version(compareto)

        if self.string == compareto.string:
            return False

        self._validate_comparison_strategy(compareto)

        return self._compare_versions(self, compareto)

    def __ne__(self, compareto: object) -> bool:
        return not self.__eq__(compareto)

    def __le__(self, compareto: object) -> bool:
        return self.__eq__(compareto) or self.__lt__(compareto)

    def __ge__(self, compareto: object) -> bool:
        return self.__eq__(compareto) or self.__gt__(compareto)

    def __sub__(self, compareto: object) -> AwesomeVersionDiff:
        return self.diff(compareto)

    def __hash__(self) -> int:
        return str.__hash__(self.string)

    def diff(self, compareto: VersionType) -> AwesomeVersionDiff:
        """Return a dictionary with differences between 2 AwesomeVersion objects."""
        compareto = self._ensure_awesome_version(compareto)
        return AwesomeVersionDiff(
            {
                "major": str(self.major) != str(compareto.major),
                "minor": str(self.minor) != str(compareto.minor),
                "patch": str(self.patch) != str(compareto.patch),
                "modifier": self.modifier != compareto.modifier,
                "strategy": self.strategy != compareto.strategy,
            }
        )

    def in_range(self, lowest: VersionType, highest: VersionType) -> bool:
        """Check if version is in range."""
        lowest = self._ensure_awesome_version(lowest, "Lowest version is not valid")
        highest = self._ensure_awesome_version(highest, "Highest version is not valid")
        return lowest <= self <= highest

    def section(self, idx: int) -> int:
        """Return the value of the specified section of the version."""
        strategy = self.strategy
        if strategy == AwesomeVersionStrategy.HEXVER:
            return int(self.string, 16) if idx == 0 else 0

        if strategy == AwesomeVersionStrategy.BUILDVER:
            if idx == 0:
                try:
                    return int(self.string)
                except ValueError:
                    return 0
            return 0

        if self.sections >= (idx + 1):
            version_parts = self.string.split(".")
            if idx < len(version_parts):
                section_str = version_parts[idx]
                match = RE_DIGIT.match(section_str or "")
                if match and match.groups():
                    return int(match.group(1) or 0)
        return 0

    @staticmethod
    def _compare_versions(version_a: AwesomeVersion, version_b: AwesomeVersion) -> bool:
        """Compare versions."""
        for handler in (
            compare_handler_container,
            compare_handler_simple,
            compare_handler_sections,
            compare_handler_semver_modifier,
        ):
            result = handler(version_a, version_b)
            if result is not None:
                return result
        return False

    @property
    def string(self) -> str:
        """Return a string representation of the version."""
        if not self._version:
            return self._version

        prefix = self.prefix

        if prefix is None:
            return self._version
        return self._version[len(prefix) :]

    @cached_property
    def prefix(self) -> str | None:
        """Return the version prefix if any"""
        version = self._version

        for prefix in ("v", "V", "v.", "V."):
            if version.startswith(prefix):
                return prefix

        return None

    @property
    def alpha(self) -> bool:
        """Return a bool to indicate alpha version."""
        return "a" in self.modifier if self.modifier else False

    @property
    def beta(self) -> bool:
        """Return a bool to indicate beta version."""
        return "b" in self.modifier if self.modifier else "beta" in self.string

    @property
    def dev(self) -> bool:
        """Return a bool to indicate dev version."""
        return "d" in self.modifier if self.modifier else "dev" in self.string

    @property
    def release_candidate(self) -> bool:
        """Return a bool to indicate release candidate version."""
        return "rc" in self.modifier if self.modifier else "rc" in self.string

    @property
    def sections(self) -> int:
        """Return a int representation of the number of sections in the version."""
        if self._sections is not None:
            return self._sections

        strategy = self.strategy
        if strategy == AwesomeVersionStrategy.SEMVER:
            self._sections = 3
        elif strategy in {
            AwesomeVersionStrategy.HEXVER,
            AwesomeVersionStrategy.SPECIALCONTAINER,
            AwesomeVersionStrategy.BUILDVER,
        }:
            self._sections = 1
        else:
            version_parts = self.string.split(".")
            modifier = self.modifier
            modifier_type = self.modifier_type

            self._sections = len(
                [
                    section.split(modifier_type)[-1] if modifier_type else section
                    for section in version_parts
                    if section and (modifier is None or section != modifier)
                ]
            )
        return self._sections

    @cached_property
    def major(self) -> AwesomeVersion | None:
        """
        Return a AwesomeVersion representation of the major version.

        Will return None if the versions is not semver/buildver/calver/simplever/pep440.
        """
        return self._get_version_section(0, MAJOR_STRATEGIES)

    @cached_property
    def minor(self) -> AwesomeVersion | None:
        """
        Return a AwesomeVersion representation of the minor version.

        Will return None if the versions is not semver/simplever/calver/pep440
        Will return None if the version does not have at least 2 sections.
        """
        return self._get_version_section(1, VERSIONED_STRATEGIES)

    @cached_property
    def patch(self) -> AwesomeVersion | None:
        """
        Return a AwesomeVersion representation of the patch version.

        Will return None if the versions is not semver/simplever/calver/pep440
        Will return None if the version does not have at least 3 sections.
        """
        return self._get_version_section(2, VERSIONED_STRATEGIES)

    @property
    def micro(self) -> AwesomeVersion | None:
        """Alias to self.patch"""
        return self.patch

    @property
    def year(self) -> AwesomeVersion | None:
        """Alias to self.major, here to provide a better name for use in CalVer."""
        return self.major

    @property
    def valid(self) -> bool:
        """Return True if the version is not UNKNOWN."""
        return self.strategy != AwesomeVersionStrategy.UNKNOWN

    @property
    def modifier(self) -> str | None:
        """Return the modifier of the version if any."""
        if self._modifier is not None:
            return self._modifier

        if self.strategy in (
            AwesomeVersionStrategy.SPECIALCONTAINER,
            AwesomeVersionStrategy.HEXVER,
        ):
            return None

        modifier_string = None

        if (
            self.strategy_description is not None
            and self.strategy_description.strategy == AwesomeVersionStrategy.SEMVER
        ):
            match = self.strategy_description.pattern.match(self.string)
            if match and len(match.groups()) >= 4:
                self._modifier = modifier_string = match.group(4)
        else:
            modifier_string = self.string.split(".")[-1]

        if not modifier_string:
            return None

        match = RE_MODIFIER.match(modifier_string)
        if match and len(match.groups()) >= 2:
            self._modifier = match.group(2)

        return self._modifier

    @property
    def modifier_type(self) -> str | None:
        """Return the modifier type of the version if any."""
        if self._modifier_type is not None:
            return self._modifier_type
        if self.strategy == AwesomeVersionStrategy.HEXVER:
            return None

        modifier = self.modifier or ""
        match = RE_MODIFIER.match(modifier)
        if match and len(match.groups()) >= 3:
            self._modifier_type = match.group(3)
        else:
            compound_match = match_compound_modifier(modifier)
            if compound_match:
                self._modifier_type = compound_match.group(1)

        return self._modifier_type

    @property
    def strategy_description(self) -> AwesomeVersionStrategyDescription | None:
        """Return a string representation of the strategy."""
        if self.strategy == AwesomeVersionStrategy.UNKNOWN:
            return None
        return VERSION_STRATEGIES_DICT[self.strategy]

    @cached_property
    def strategy(self) -> AwesomeVersionStrategy:
        """Return the version strategy."""
        version_str = self.string
        if version_str:
            fast_path_strategy = None

            if version_str in ("latest", "dev", "stable", "beta"):
                fast_path_strategy = AwesomeVersionStrategy.SPECIALCONTAINER

            elif version_str.startswith("0x") and len(version_str) > 2:
                hex_part = version_str[2:]
                if all(c in "0123456789ABCDEFabcdef" for c in hex_part):
                    fast_path_strategy = AwesomeVersionStrategy.HEXVER

            elif version_str.isdigit():
                fast_path_strategy = AwesomeVersionStrategy.BUILDVER

            if fast_path_strategy is not None:
                if (
                    not self._ensure_strategy
                    or fast_path_strategy in self._ensure_strategy
                ):
                    return fast_path_strategy

        version_strategies: dict[
            AwesomeVersionStrategy, AwesomeVersionStrategyDescription
        ] = {}

        for strategy in self._ensure_strategy or []:
            version_strategies[strategy] = VERSION_STRATEGIES_DICT[strategy]

        for description in VERSION_STRATEGIES:
            if description.strategy not in version_strategies:
                version_strategies[description.strategy] = description

        for description in version_strategies.values():
            if description.pattern.match(self.string) is not None and (
                description.validate is None or description.validate(self.string)
            ):
                return description.strategy
        return AwesomeVersionStrategy.UNKNOWN

    @cached_property
    def simple(self) -> bool:
        """Return True if the version string is simple."""
        return generate_full_string_regex(RE_SIMPLE).match(self.string) is not None

    def _ensure_awesome_version(
        self, version: VersionType, error_msg: str = "Not a valid AwesomeVersion object"
    ) -> AwesomeVersion:
        """Convert input to AwesomeVersion if needed, with validation."""
        if isinstance(version, AwesomeVersion):
            return version
        if isinstance(version, (str, float, int)):
            return AwesomeVersion(version)
        raise AwesomeVersionCompareException(error_msg)

    def _validate_comparison_strategy(self, other: AwesomeVersion) -> None:
        """Validate that both versions can be compared."""
        if AwesomeVersionStrategy.UNKNOWN in (self.strategy, other.strategy):
            raise AwesomeVersionCompareException(
                f"Can't compare <{self.strategy.value} {self._version}> and "
                f"<{other.strategy.value} {other.string}>"
            )

    def _get_version_section(
        self,
        section_index: int,
        valid_strategies: frozenset[AwesomeVersionStrategy],
    ) -> AwesomeVersion | None:
        """Helper method to get version section if strategy and section count are valid."""
        if self.strategy not in valid_strategies:
            return None
        if section_index > 0 and self.sections < (section_index + 1):
            return None
        return AwesomeVersion(self.section(section_index))


class AwesomeVersionDiff:
    """Structured output of AwesomeVersion.diff"""

    def __init__(self, changes: Dict[str, bool]) -> None:
        """Initialize the AwesomeVersionDiff."""
        self._changes = changes

    def __repr__(self) -> str:
        return (
            f"AwesomeVersionDiff(major={self.major}, minor={self.minor}, "
            f"patch={self.patch}, modifier={self.modifier}, strategy={self.strategy})"
        )

    @property
    def major(self) -> bool:
        """Return True if the major version has changed."""
        return self._changes["major"]

    @property
    def minor(self) -> bool:
        """Return True if the minor version has changed."""
        return self._changes["minor"]

    @property
    def patch(self) -> bool:
        """Return True if the patch version has changed."""
        return self._changes["patch"]

    @property
    def modifier(self) -> bool:
        """Return True if the modifier version has changed."""
        return self._changes["modifier"]

    @property
    def strategy(self) -> bool:
        """Return True if the strategy has changed."""
        return self._changes["strategy"]
