"""Compare handlers"""

from copy import copy
from typing import TYPE_CHECKING, Optional

from .comparehandlers.base import AwesomeVersionCompareHandler
from .comparehandlers.container import AwesomeVersionCompareHandlerContainer
from .comparehandlers.devrc import AwesomeVersionCompareHandlerDevRc
from .comparehandlers.modifier import AwesomeVersionCompareHandlerSemVerModifier
from .comparehandlers.sections import AwesomeVersionCompareHandlerSections
from .comparehandlers.simple import AwesomeVersionCompareHandlerSimple
from .const import LOGGER
from .exceptions import AwesomeVersionCustomHandlerException

if TYPE_CHECKING:
    from .awesomeversion import AwesomeVersion


class CompareHandlers:
    """CompareHandlers class."""

    def __init__(
        self, version_a: "AwesomeVersion", version_b: "AwesomeVersion"
    ) -> None:
        """Initialize the special handler base_class."""
        self.version_a = copy(version_a)
        self.version_b = copy(version_b)

    def check(
        self,
        custom_compare_handlers: Optional[list[AwesomeVersionCompareHandler]] = None,
    ) -> bool:
        """Handler."""
        handlers = custom_compare_handlers or []
        handlers.extend(
            [
                AwesomeVersionCompareHandlerContainer,
                AwesomeVersionCompareHandlerSimple,
                AwesomeVersionCompareHandlerDevRc,
                AwesomeVersionCompareHandlerSemVerModifier,
                AwesomeVersionCompareHandlerSections,
            ]
        )

        for handler in handlers:
            try:
                is_valid = issubclass(handler, AwesomeVersionCompareHandler)
            except TypeError:
                is_valid = False

            if not is_valid:
                raise AwesomeVersionCustomHandlerException(
                    f"{handler.__class__.__bases__} Is not correct."
                )

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
                result: Optional[bool] = compare.handler()
                if result is not None:
                    return result
