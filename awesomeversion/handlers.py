"""Compare handlers"""
from copy import copy
from typing import TYPE_CHECKING, List, Optional, Type

from awesomeversion.comparehandlers.base import CompareHandlerBase

from .comparehandlers.container import ComparelHandlerContainer
from .comparehandlers.devrc import ComparelHandlerDevRc
from .comparehandlers.modifier import ComparelHandlerSemVerModifier
from .comparehandlers.sections import ComparelHandlerSections
from .comparehandlers.simple import ComparelHandlerSimple
from .utils.logger import LOGGER

if TYPE_CHECKING:
    from .awesomeversion import AwesomeVersion


HANDLERS: List[Type[CompareHandlerBase]] = [
    ComparelHandlerContainer,
    ComparelHandlerSimple,
    ComparelHandlerDevRc,
    ComparelHandlerSemVerModifier,
    ComparelHandlerSections,
]


class CompareHandlers:
    """CompareHandlers class."""

    def __init__(self, ver_a: "AwesomeVersion", ver_b: "AwesomeVersion") -> None:
        """Initialize the special handler base_class."""
        self.ver_a = ver_a
        self.ver_b = ver_b

    def check(self) -> bool:
        """Handler."""
        for handler in HANDLERS:
            result = self.check_handler(handler)
            if result is not None:
                return result

        return False

    def check_handler(self, handler: Type[CompareHandlerBase]) -> Optional[bool]:
        """Check with spesific handler."""
        ver_a, ver_b = copy(self.ver_a), copy(self.ver_b)
        compare_handler = handler(ver_a, ver_b)
        LOGGER.debug(
            "Comparing '%s' against '%s' with '%s'", ver_a, ver_b, handler.__name__
        )
        if len(compare_handler.strategy) == 0 or (
            self.ver_a.strategy in compare_handler.strategy
            and self.ver_b.strategy in compare_handler.strategy
        ):
            result = compare_handler.handler()
            if result is not None:
                return result
        return None
