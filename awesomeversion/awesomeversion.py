"""AwesomeVersion."""
# pylint: disable=unused-argument
import logging
from typing import List, Optional, Union

from .exceptions import AwesomeVersionCompare, AwesomeVersionStrategyException
from .handlers import CompareHandlers
from .match import (
    RE_DIGIT,
    RE_MODIFIER,
    RE_SEMVER,
    RE_VERSION,
    is_simple,
    version_strategy,
)
from .strategy import AwesomeVersionStrategy

_LOGGER: logging.Logger = logging.getLogger(__package__)


class _AwesomeVersionBase(str):
    """Base class for AwesomeVersion to allow the usage of the default JSON encoder."""

    def __init__(self, string):
        str.__init__(string)

    def __new__(cls, version, _=None):
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

    def __init__(
        self,
        version: Union[str, float, int, "AwesomeVersion"],
        ensure_strategy: Optional[
            Union[AwesomeVersionStrategy, List[AwesomeVersionStrategy]]
        ] = None,
    ) -> None:
        """Initialize AwesomeVersion."""
        if isinstance(version, AwesomeVersion):
            self._version = version._version
        else:
            self._version = str(version)
        if isinstance(self._version, str):
            self._version = self._version.strip()

        if ensure_strategy is not None:
            ensure_strategy = (
                ensure_strategy
                if isinstance(ensure_strategy, list)
                else [ensure_strategy]
            )
            if self.strategy not in ensure_strategy:
                raise AwesomeVersionStrategyException(
                    f"Strategy {self.strategy} does not match {ensure_strategy} for {version}"
                )

        super().__init__(self._version)

    def __enter__(self) -> "AwesomeVersion":
        return self

    def __exit__(self, *exc_info) -> None:
        pass

    def __repr__(self) -> str:
        return f"<AwesomeVersion {self.strategy} '{self.string}'>"

    def __str__(self) -> str:
        return str(self._version)

    def __eq__(self, compareto: Union[str, float, int, "AwesomeVersion"]) -> bool:
        """Check if equals to."""
        if isinstance(compareto, (str, float, int)):
            compareto = AwesomeVersion(compareto)
        if not isinstance(compareto, AwesomeVersion):
            raise AwesomeVersionCompare("Not a valid AwesomeVersion object")
        return self.string == compareto.string

    def __lt__(self, compareto: Union[str, float, int, "AwesomeVersion"]) -> bool:
        """Check if less than."""
        if isinstance(compareto, (str, float, int)):
            compareto = AwesomeVersion(compareto)
        if not isinstance(compareto, AwesomeVersion):
            raise AwesomeVersionCompare("Not a valid AwesomeVersion object")
        if (self.strategy == AwesomeVersionStrategy.UNKNOWN) or (
            compareto.strategy == AwesomeVersionStrategy.UNKNOWN
        ):
            raise AwesomeVersionCompare(
                f"Can't compare {AwesomeVersionStrategy.UNKNOWN}"
            )
        return CompareHandlers(compareto, self).check()

    def __gt__(self, compareto: Union[str, float, int, "AwesomeVersion"]) -> bool:
        """Check if greater than."""
        if isinstance(compareto, (str, float, int)):
            compareto = AwesomeVersion(compareto)
        if not isinstance(compareto, AwesomeVersion):
            raise AwesomeVersionCompare("Not a valid AwesomeVersion object")
        if (self.strategy == AwesomeVersionStrategy.UNKNOWN) or (
            compareto.strategy == AwesomeVersionStrategy.UNKNOWN
        ):
            raise AwesomeVersionCompare(
                f"Can't compare {AwesomeVersionStrategy.UNKNOWN}"
            )
        return CompareHandlers(self, compareto).check()

    def __ne__(self, compareto: "AwesomeVersion") -> bool:
        return not self.__eq__(compareto)

    def __le__(self, compareto: "AwesomeVersion") -> bool:
        return self.__eq__(compareto) or self.__lt__(compareto)

    def __ge__(self, compareto: "AwesomeVersion") -> bool:
        return self.__eq__(compareto) or self.__gt__(compareto)

    def section(self, idx: int) -> int:
        """Return the value of the specified section of the version."""
        if self.sections >= (idx + 1):
            return int(RE_DIGIT.match(self.string.split(".")[idx]).group(1))
        return 0

    @staticmethod
    def ensure_strategy(
        version: Union[str, float, int, "AwesomeVersion"],
        strategy: Union[AwesomeVersionStrategy, List[AwesomeVersionStrategy]],
    ) -> "AwesomeVersion":
        """Return a AwesomeVersion object, or raise on creation."""
        _LOGGER.warning(
            "Using AwesomeVersion.ensure_strategy(version, strategy) is deprecated, "
            "use AwesomeVersion(version, strategy) instead"
        )
        return AwesomeVersion(version, strategy)

    @property
    def string(self) -> str:
        """Return a string representaion of the version."""
        if self._version.endswith("."):
            self._version = self._version[:-1]
        version = RE_VERSION.match(str(self._version)).group(2)
        return version

    @property
    def prefix(self) -> Optional[str]:
        """Return the version prefix if any"""
        return RE_VERSION.match(str(self._version)).group(1)

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
    def modifier(self) -> str:
        """Return the modifier of the version if any."""
        if self.strategy == AwesomeVersionStrategy.SEMVER:
            match = RE_MODIFIER.match(RE_SEMVER.match(self.string).group(4) or "")
        elif self.strategy == AwesomeVersionStrategy.SPECIALCONTAINER:
            return None
        else:
            match = RE_MODIFIER.match(self.string.split(".")[-1])
        return match.group(2) if match else None

    @property
    def modifier_type(self) -> str:
        """Return the modifier type of the version if any."""
        if self.strategy == AwesomeVersionStrategy.SEMVER:
            match = RE_MODIFIER.match(RE_SEMVER.match(self.string).group(4) or "")
        elif self.strategy == AwesomeVersionStrategy.SPECIALCONTAINER:
            return None
        else:
            match = RE_MODIFIER.match(self.string.split(".")[-1])
        return match.group(3) if match else None

    @property
    def strategy(self) -> AwesomeVersionStrategy:
        """Return the version strategy."""
        return version_strategy(self.string)

    @property
    def simple(self) -> bool:
        """Return True if the version string is simple."""
        return is_simple(self.string)
