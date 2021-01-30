"""Compare handlers"""
import logging
from copy import copy
from typing import TYPE_CHECKING, Optional

from .comparehandlers.container import ComparelHandlerContainer
from .comparehandlers.dev import ComparelHandlerDev
from .comparehandlers.modifier import ComparelHandlerSemVerModifier
from .comparehandlers.sections import ComparelHandlerSections
from .comparehandlers.simple import ComparelHandlerSimple

_LOGGER: logging.Logger = logging.getLogger(__package__)

if TYPE_CHECKING:
    from .awesomeversion import AwesomeVersion


class CompareHandlers:
    """CompareHandlers class."""

    def __init__(self, ver_a: "AwesomeVersion", ver_b: "AwesomeVersion") -> None:
        """Initialize the special handler base_class."""
        self.ver_a = copy(ver_a)
        self.ver_b = copy(ver_b)

    def check(self) -> bool:
        """Handler."""
        handlers = [
            ComparelHandlerContainer,
            ComparelHandlerSimple,
            ComparelHandlerDev,
            ComparelHandlerSemVerModifier,
            ComparelHandlerSections,
        ]

        for handler in handlers:
            ver_a, ver_b = self.ver_a, self.ver_b
            compare = handler(ver_a, ver_b)
            _LOGGER.debug(
                "Comparing '%s' against '%s' with '%s'", ver_a, ver_b, handler.__name__
            )
            if len(compare.strategy) == 0 or (
                self.ver_a.strategy in compare.strategy
                and self.ver_b.strategy in compare.strategy
            ):
                result: Optional[bool] = compare.handler()
                if result is not None:
                    return result
