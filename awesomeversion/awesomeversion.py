"""AwesomeVersion."""
from types import TracebackType
from typing import Dict, List, Optional, Pattern, Type, Union

from .exceptions import AwesomeVersionCompareException, AwesomeVersionStrategyException
from .handlers import CompareHandlers
from .strategy import VERSION_STRATEGIES, AwesomeVersionStrategy
from .typing import EnsureStrategyIterableType, EnsureStrategyType, VersionType
from .utils.logger import LOGGER
from .utils.regex import (
    RE_DIGIT,
    RE_MODIFIER,
    RE_SEMVER,
    RE_SIMPLE,
    RE_VERSION,
    get_regex_match_group,
    is_regex_matching,
)


class _AwesomeVersionBase(str):
    """Base class for AwesomeVersion to allow the usage of the default JSON encoder."""

    def __init__(self, string: str):
        str.__init__(string)

    def __new__(
        cls,
        version: str,
        ensure_strategy: EnsureStrategyType = None,  # pylint: disable=unused-argument
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
    """

    _version: str = ""
    _ensure_strategy: EnsureStrategyIterableType = []

    def __init__(
        self,
        version: VersionType,
        ensure_strategy: EnsureStrategyType = None,
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
            if self.strategy not in ensure_strategy:
                raise AwesomeVersionStrategyException(
                    f"Strategy {self.strategy} does not match {ensure_strategy} for {version}"
                )

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
        return f"<AwesomeVersion {self.strategy} '{self.string}'>"

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
                f"Can't compare {self.strategy} and {compareto.strategy}"
            )
        return CompareHandlers(compareto, self).check()

    def __gt__(self, compareto: VersionType) -> bool:
        """Check if greater than."""
        if isinstance(compareto, (str, float, int)):
            compareto = AwesomeVersion(compareto)
        if not isinstance(compareto, AwesomeVersion):
            raise AwesomeVersionCompareException("Not a valid AwesomeVersion object")
        if AwesomeVersionStrategy.UNKNOWN in (self.strategy, compareto.strategy):
            raise AwesomeVersionCompareException(
                f"Can't compare {self.strategy} and {compareto.strategy}"
            )
        return CompareHandlers(self, compareto).check()

    def __ne__(self, compareto: object) -> bool:
        return not self.__eq__(compareto)

    def __le__(self, compareto: object) -> bool:
        return self.__eq__(compareto) or self.__lt__(compareto)

    def __ge__(self, compareto: object) -> bool:
        return self.__eq__(compareto) or self.__gt__(compareto)

    def section(self, idx: int) -> int:
        """Return the value of the specified section of the version."""
        if self.sections >= (idx + 1):
            match = get_regex_match_group(RE_DIGIT, (self.string.split(".")[idx]), 1)
            if match:
                return int(match)
        return 0

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
        if self._version.endswith("."):
            self._version = self._version[:-1]
        version = get_regex_match_group(RE_VERSION, str(self._version), 2)
        return version or self._version

    @property
    def prefix(self) -> Optional[str]:
        """Return the version prefix if any"""
        return get_regex_match_group(RE_VERSION, str(self._version), 1)

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

        if self.strategy == AwesomeVersionStrategy.SEMVER:
            modifier_string = get_regex_match_group(RE_SEMVER, str(self.string), 4)
        else:
            modifier_string = self.string.split(".")[-1]

        return get_regex_match_group(RE_MODIFIER, modifier_string, 2)

    @property
    def modifier_type(self) -> Optional[str]:
        """Return the modifier type of the version if any."""
        if self.strategy == AwesomeVersionStrategy.SPECIALCONTAINER:
            return None

        if self.strategy == AwesomeVersionStrategy.SEMVER:
            modifier_string = get_regex_match_group(RE_SEMVER, str(self.string), 4)
        else:
            modifier_string = self.string.split(".")[-1]

        return get_regex_match_group(RE_MODIFIER, modifier_string, 3)

    @property
    def strategy(self) -> AwesomeVersionStrategy:
        """Return the version strategy."""
        version_strategies: Dict[AwesomeVersionStrategy, Pattern[str]] = {}

        for strategy in self._ensure_strategy or []:
            version_strategies[strategy] = VERSION_STRATEGIES[strategy]

        for (strategy, pattern) in VERSION_STRATEGIES.items():
            if strategy not in version_strategies:
                version_strategies[strategy] = pattern

        for (strategy, pattern) in version_strategies.items():
            if is_regex_matching(pattern, self.string):
                return strategy

        return AwesomeVersionStrategy.UNKNOWN

    @property
    def simple(self) -> bool:
        """Return True if the version string is simple."""
        return is_regex_matching(RE_SIMPLE, self.string)
