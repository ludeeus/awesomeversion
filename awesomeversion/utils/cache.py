"""This module contains the ValueCache class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .unset import UNSET_VALUE

if TYPE_CHECKING:
    from ..awesomeversion import AwesomeVersion


class ValueCache:
    def __init__(self):
        self.__prefix: str | None | object = UNSET_VALUE
        self.__major: AwesomeVersion | None | object = UNSET_VALUE
        self.__minor: AwesomeVersion | None | object = UNSET_VALUE
        self.__patch: AwesomeVersion | None | object = UNSET_VALUE

    @property
    def prefix(self) -> str | None | object:
        """Get the prefix."""
        return self.__prefix

    @prefix.setter
    def prefix(self, value: str | None) -> None:
        """Set the prefix."""
        self.__prefix = value

    @property
    def major(self) -> AwesomeVersion | None | object:
        """Get the major."""
        return self.__major

    @major.setter
    def major(self, value: AwesomeVersion | None) -> None:
        """Set the major."""
        self.__major = value

    @property
    def minor(self) -> AwesomeVersion | None | object:
        """Get the minor."""
        return self.__minor

    @minor.setter
    def minor(self, value: AwesomeVersion | None) -> None:
        """Set the minor."""
        self.__minor = value

    @property
    def patch(self) -> AwesomeVersion | None | object:
        """Get the patch."""
        return self.__patch

    @patch.setter
    def patch(self, value: AwesomeVersion | None) -> None:
        """Set the patch."""
        self.__patch = value
