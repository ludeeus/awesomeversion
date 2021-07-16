"""Compare handlers"""
from __future__ import annotations
from copy import copy
from typing import TYPE_CHECKING

from .comparehandlers.container import ComparelHandlerContainer
from .comparehandlers.devrc import ComparelHandlerDevRc
from .comparehandlers.modifier import ComparelHandlerSemVerModifier
from .comparehandlers.sections import ComparelHandlerSections
from .comparehandlers.simple import ComparelHandlerSimple
from .const import LOGGER

if TYPE_CHECKING:
    from .awesomeversion import AwesomeVersion


class CompareHandlers:
    """CompareHandlers class."""

    def __init__(self, version_a: AwesomeVersion, version_b: AwesomeVersion) -> None:
        """Initialize the special handler base_class."""
        self.version_a = copy(version_a)
        self.version_b = copy(version_b)

    def check(self) -> bool:
        """Handler."""
        handlers = [
            ComparelHandlerContainer,
            ComparelHandlerSimple,
            ComparelHandlerDevRc,
            ComparelHandlerSemVerModifier,
            ComparelHandlerSections,
        ]

        for handler in handlers:
            version_a, version_b = self.version_a, self.version_b
            compare = handler(version_a, version_b)
            LOGGER.debug(
                "Comparing '%s' against '%s' with '%s'",
                version_a,
                version_b,
                handler.__name__,
            )

            if len(compare.strategy) == 0 or (
                self.version_a.strategy in compare.strategy
                and self.version_b.strategy in compare.strategy
            ):
                result: bool | None = compare.handler()
                if result is not None:
                    return result
