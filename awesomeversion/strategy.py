"""For backwards compability, will be removed in the first release of 2022"""
from .const import LOGGER, AwesomeVersionStrategy

LOGGER.warning(
    "Importing AwesomeVersionStrategy from awesomeversion.strategy is deprecated, "
    "import it from awesomeversion instead"
)
