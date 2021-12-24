"""AwesomeVersion."""
from types import TracebackType
from typing import Any, Dict, List, Optional, Type, Union

from .comparehandlers.container import compare_handler_container
from .comparehandlers.devrc import compare_handler_devrc
from .comparehandlers.modifier import compare_handler_semver_modifier
from .comparehandlers.sections import compare_handler_sections
from .comparehandlers.simple import compare_handler_simple
from .exceptions import AwesomeVersionCompareException, AwesomeVersionStrategyException
from .strategy import (
    VERSION_STRATEGIES,
    VERSION_STRATEGIES_DICT,
    AwesomeVersionStrategy,
    AwesomeVersionStrategyDescription,
)
from .typing import EnsureStrategyIterableType, EnsureStrategyType, VersionType
from .utils.logger import LOGGER
from .utils.regex import (
    RE_DIGIT,
    RE_MODIFIER,
    RE_SIMPLE,
    compile_regex,
    generate_full_string_regex,
)


class _AwesomeVersionBase(str):
    """Base class for AwesomeVersion to allow the usage of the default JSON encoder."""

    def __init__(self, string: str):
        str.__init__(string)

    def __new__(
        cls,
        version: str,
        *_: Optional[Any],
        **__: Optional[Any],
    ) -> "_AwesomeVersionBase":
        """Create a new AwesomeVersion object."""

        return super().__new__(cls, version)


class AwesomeVersion(_AwesomeVersionBase):
    """
    AwesomeVersion class.

    version:
        The version to create a AwesomeVersion object from

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

    _version: str = ""
    _ensure_strategy: EnsureStrategyIterableType = []

    def __init__(
        self,
        version: VersionType,
        ensure_strategy: EnsureStrategyType = None,
        find_first_match: bool = False,
    ) -> None:
        """Initialize AwesomeVersion."""
        if isinstance(version, AwesomeVersion):
            self._version = version._version
        else:
            self._version = str(version)
        if isinstance(self._version, str):
            self._version = self._version.strip()

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

            if self.strategy not in ensure_strategy:
                raise AwesomeVersionStrategyException(
                    f"Strategy {self.strategy.value} does not match "
                    f"{[strategy.value for strategy in ensure_strategy]} for {version}"
                )

        if self._version and self._version[-1] == ".":
            self._version = self._version[:-1]

        super().__init__(self._version)

    def __enter__(self) -> "AwesomeVersion":
        return self

    def __exit__(
        self,
        exctype: Optional[Type[BaseException]],
        excinst: Optional[BaseException],
        exctb: Optional[TracebackType],
    ) -> bool:
        pass

    def __repr__(self) -> str:
        return f"<AwesomeVersion {self.strategy.value} '{self.string}'>"

    def __str__(self) -> str:
        return str(self._version)

    def __eq__(self, compareto: VersionType) -> bool:
        """Check if equals to."""
        if isinstance(compareto, (str, float, int)):
            compareto = AwesomeVersion(compareto)
        if not isinstance(compareto, AwesomeVersion):
            raise AwesomeVersionCompareException("Not a valid AwesomeVersion object")
        return self.string == compareto.string

    def __lt__(self, compareto: VersionType) -> bool:
        """Check if less than."""
        if isinstance(compareto, (str, float, int)):
            compareto = AwesomeVersion(compareto)
        if not isinstance(compareto, AwesomeVersion):
            raise AwesomeVersionCompareException("Not a valid AwesomeVersion object")
        if AwesomeVersionStrategy.UNKNOWN in (self.strategy, compareto.strategy):
            raise AwesomeVersionCompareException(
                f"Can't compare {self.strategy.value} and {compareto.strategy.value}"
            )
        return self.string != compareto.string and self._compare_versions(
            compareto, self
        )

    def __gt__(self, compareto: VersionType) -> bool:
        """Check if greater than."""
        if isinstance(compareto, (str, float, int)):
            compareto = AwesomeVersion(compareto)
        if not isinstance(compareto, AwesomeVersion):
            raise AwesomeVersionCompareException("Not a valid AwesomeVersion object")
        if AwesomeVersionStrategy.UNKNOWN in (self.strategy, compareto.strategy):
            raise AwesomeVersionCompareException(
                f"Can't compare {self.strategy.value} and {compareto.strategy.value}"
            )
        return self.string != compareto.string and self._compare_versions(
            self, compareto
        )

    def __ne__(self, compareto: object) -> bool:
        return not self.__eq__(compareto)

    def __le__(self, compareto: object) -> bool:
        return self.__eq__(compareto) or self.__lt__(compareto)

    def __ge__(self, compareto: object) -> bool:
        return self.__eq__(compareto) or self.__gt__(compareto)

    def section(self, idx: int) -> int:
        """Return the value of the specified section of the version."""
        if self.sections >= (idx + 1):
            match = RE_DIGIT.match(self.string.split(".")[idx] or "")
            if match and match.groups():
                return int(match.group(1))
        return 0

    @staticmethod
    def _compare_versions(version_a: str, version_b: str) -> bool:
        """Compare versions."""
        for handler in (
            compare_handler_container,
            compare_handler_simple,
            compare_handler_devrc,
            compare_handler_semver_modifier,
            compare_handler_sections,
        ):
            LOGGER.debug(
                "Comparing '%s' against '%s' with '%s'",
                version_a,
                version_b,
                handler.__name__,
            )
            result = handler(AwesomeVersion(version_a), AwesomeVersion(version_b))
            if result is not None:
                return result
        return False

    @staticmethod
    def ensure_strategy(
        version: Union[str, float, int, "AwesomeVersion"],
        strategy: Union[AwesomeVersionStrategy, List[AwesomeVersionStrategy]],
    ) -> "AwesomeVersion":
        """Return a AwesomeVersion object, or raise on creation."""
        LOGGER.warning(
            "Using AwesomeVersion.ensure_strategy(version, strategy) is deprecated, "
            "use AwesomeVersion(version, strategy) instead"
        )
        return AwesomeVersion(version, strategy)

    @property
    def string(self) -> str:
        """Return a string representaion of the version."""
        if not self._version:
            return self._version

        prefix = self.prefix

        if prefix is None:
            return self._version
        return self._version[len(prefix) :]

    @property
    def prefix(self) -> Optional[str]:
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
        """Return a int representaion of the number of sections in the version."""
        if self.strategy == AwesomeVersionStrategy.SEMVER:
            return 3
        return len(self.string.split("."))

    @property
    def major(self) -> Optional["AwesomeVersion"]:
        """Return a AwesomeVersion representation of the major version."""
        if self.strategy != AwesomeVersionStrategy.SEMVER:
            return None
        return AwesomeVersion(self.section(0))

    @property
    def minor(self) -> Optional["AwesomeVersion"]:
        """Return a AwesomeVersion representation of the minor version."""
        if self.strategy != AwesomeVersionStrategy.SEMVER:
            return None
        return AwesomeVersion(self.section(1))

    @property
    def patch(self) -> Optional["AwesomeVersion"]:
        """Return a AwesomeVersion representation of the patch version."""
        if self.strategy != AwesomeVersionStrategy.SEMVER:
            return None
        return AwesomeVersion(self.section(2))

    @property
    def modifier(self) -> Optional[str]:
        """Return the modifier of the version if any."""
        if self.strategy == AwesomeVersionStrategy.SPECIALCONTAINER:
            return None

        modifier_string = None

        if (
            self.strategy_description is not None
            and self.strategy_description.strategy == AwesomeVersionStrategy.SEMVER
        ):
            match = self.strategy_description.pattern.match(self.string)
            if match and len(match.groups()) >= 4:
                modifier_string = match.group(4)

        else:
            modifier_string = self.string.split(".")[-1]

        if not modifier_string:
            return None

        match = RE_MODIFIER.match(modifier_string)
        if match and len(match.groups()) >= 2:
            return match.group(2)

        return None

    @property
    def modifier_type(self) -> Optional[str]:
        """Return the modifier type of the version if any."""
        match = RE_MODIFIER.match(self.modifier or "")
        if match and len(match.groups()) >= 3:
            return match.group(3)

        return None

    @property
    def strategy_description(self) -> Optional[AwesomeVersionStrategyDescription]:
        """Return a string representation of the strategy."""
        if self.strategy == AwesomeVersionStrategy.UNKNOWN:
            return None
        return VERSION_STRATEGIES_DICT[self.strategy]

    @property
    def strategy(self) -> AwesomeVersionStrategy:
        """Return the version strategy."""
        version_strategies: Dict[
            AwesomeVersionStrategy, AwesomeVersionStrategyDescription
        ] = {}

        for strategy in self._ensure_strategy or []:
            version_strategies[strategy] = VERSION_STRATEGIES_DICT[strategy]

        for description in VERSION_STRATEGIES:
            if description.strategy not in version_strategies:
                version_strategies[description.strategy] = description

        for description in version_strategies.values():
            if description.pattern.match(self.string) is not None:
                return description.strategy

        return AwesomeVersionStrategy.UNKNOWN

    @property
    def simple(self) -> bool:
        """Return True if the version string is simple."""
        return generate_full_string_regex(RE_SIMPLE).match(self.string) is not None
