"""AwesomeVersion."""
import logging

from .exceptions import AwesomeVersionCompare
from .match import RE_DIGIT, RE_MODIFIER, RE_VERSION, is_simple, version_strategy
from .strategy import AwesomeVersionStrategy

_LOGGER: logging.Logger = logging.getLogger(__package__)


class AwesomeVersion:
    """AwesomeVersion class."""

    def __init__(self, version: any) -> None:
        """Initialize AwesomeVersion."""
        if isinstance(version, AwesomeVersion):
            self._version = version.string
        else:
            self._version = version

    def __repr__(self) -> str:
        return f"<AwesomeVersion {self.strategy} '{self.string}'>"

    def __eq__(self, compareto: "AwesomeVersion") -> bool:
        """Check if equals to."""
        if not isinstance(compareto, AwesomeVersion):
            raise AwesomeVersionCompare("Not a valid AwesomeVersion object")
        return self.string == compareto.string

    def __lt__(self, compareto: "AwesomeVersion") -> bool:
        """Check if less than."""
        if not isinstance(compareto, AwesomeVersion):
            raise AwesomeVersionCompare("Not a valid AwesomeVersion object")
        if (self.strategy == AwesomeVersionStrategy.UNKNOWN) or (
            compareto.strategy == AwesomeVersionStrategy.UNKNOWN
        ):
            raise AwesomeVersionCompare(
                f"Can't compare {AwesomeVersionStrategy.UNKNOWN}"
            )
        return self._a_is_greater_than_b(compareto, self)

    def __gt__(self, compareto: "AwesomeVersion") -> bool:
        """Check if greater than."""
        if not isinstance(compareto, AwesomeVersion):
            raise AwesomeVersionCompare("Not a valid AwesomeVersion object")
        if (self.strategy == AwesomeVersionStrategy.UNKNOWN) or (
            compareto.strategy == AwesomeVersionStrategy.UNKNOWN
        ):
            raise AwesomeVersionCompare(
                f"Can't compare {AwesomeVersionStrategy.UNKNOWN}"
            )
        return self._a_is_greater_than_b(self, compareto)

    @property
    def string(self) -> str:
        """Return a string representaion of the version."""
        version = RE_VERSION.match(str(self._version)).group(1)
        if version.endswith("."):
            version = version[:-1]
        return version

    @property
    def alpha(self) -> bool:
        """Return a bool to indicate alpha version."""
        return "a" in self.modifier if self.modifier else False

    @property
    def beta(self) -> bool:
        """Return a bool to indicate beta version."""
        return "b" in self.modifier if self.modifier else False

    @property
    def dev(self) -> bool:
        """Return a bool to indicate dev version."""
        return "d" in self.modifier if self.modifier else False

    @property
    def release_candidate(self) -> bool:
        """Return a bool to indicate release candidate version."""
        return "rc" in self.modifier if self.modifier else False

    @property
    def sections(self) -> int:
        """Return a int representaion of the number of sections in the version."""
        return len(self.string.split("."))

    @property
    def modifier(self) -> str:
        """Return the modifier of the version if any."""
        match = RE_MODIFIER.match(self.string.split(".")[-1])
        return match.group(1) if match else None

    @property
    def strategy(self) -> AwesomeVersionStrategy:
        """Return the version strategy."""
        return version_strategy(self.string)

    @property
    def simple(self) -> bool:
        """Return True if the version string is simple."""
        return is_simple(self.string)

    def section(self, idx: int) -> int:
        """Return the value of the specified section of the version."""
        if self.sections >= (idx + 1):
            return int(RE_DIGIT.match(self.string.split(".")[idx]).group(1))
        return 0

    def _a_is_greater_than_b(
        self, ver_a: "AwesomeVersion", ver_b: "AwesomeVersion"
    ) -> bool:
        """Compare two AwesomeVersion objects against eachother."""
        _LOGGER.debug("Comparing '%s' against '%s'", ver_a.string, ver_b.string)
        a_last = ver_a.string.split(".")[-1]
        b_last = ver_b.string.split(".")[-1]
        biggest = ver_a.sections if ver_a.sections >= ver_b.sections else ver_b.sections
        if ver_a.simple and ver_b.simple:
            for section in range(0, biggest):
                if ver_a.section(section) > ver_b.section(section):
                    return True

        if not a_last.startswith("dev") and b_last.startswith("dev"):
            ver_b = AwesomeVersion(ver_b.string.replace(b_last, "0"))
            if ver_a.string == ver_b.string:
                return True

        if not ver_a.modifier and ver_b.modifier:
            new_version = AwesomeVersion(ver_b.string.replace(ver_b.modifier, ""))
            if ver_a.string == new_version.string:
                return True
            return self._a_is_greater_than_b(ver_a, new_version)

        if ver_a.modifier and not ver_b.modifier:
            new_version = AwesomeVersion(ver_a.string.replace(ver_a.modifier, ""))
            return self._a_is_greater_than_b(new_version, ver_b)

        for section in range(0, biggest):
            if ver_a.section(section) > ver_b.section(section):
                return True

        return False
