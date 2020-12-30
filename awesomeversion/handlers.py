"""Compare handlers"""
import logging
from typing import TYPE_CHECKING

from .comparehandlers.container import ComparelHandlerContainer
from .comparehandlers.dev import ComparelHandlerDev
from .comparehandlers.modifier import ComparelHandlerModifier
from .comparehandlers.sections import ComparelHandlerSections
from .comparehandlers.simple import ComparelHandlerSimple

_LOGGER: logging.Logger = logging.getLogger(__package__)

if TYPE_CHECKING:
    from .awesomeversion import AwesomeVersion


class CompareHandlers:
    def __init__(self, ver_a: "AwesomeVersion", ver_b: "AwesomeVersion") -> None:
        """Initialize the special handler base_class."""
        self.ver_a = ver_a
        self.ver_b = ver_b

    def check(self) -> bool:
        """Handler."""
        _LOGGER.debug("Comparing '%s' against '%s'", self.ver_a, self.ver_b)
        handlers = [
            ComparelHandlerSimple,
            ComparelHandlerDev,
            ComparelHandlerModifier,
            ComparelHandlerContainer,
            ComparelHandlerSections,
        ]

        for handler in handlers:
            compare = handler(self.ver_a, self.ver_b)
            if len(compare.strategy) == 0 or (
                self.ver_a.strategy in compare.strategy
                or self.ver_b.strategy in compare.strategy
            ):
                result = compare.handler()
                if result is not None:
                    return result
