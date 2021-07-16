"""Exceptions for AwesomeVersion."""


class AwesomeVersionException(Exception):
    """Base AwesomeVersion exception."""


class AwesomeVersionCompare(AwesomeVersionException):
    """Thrown when compare is not possible."""


class AwesomeVersionStrategyException(AwesomeVersionException):
    """Thrown when the expected strategy does not match."""


class AwesomeVersionCustomStrategyException(AwesomeVersionStrategyException):
    """Thrown when the custom strategy is not configured properly."""


class AwesomeVersionCustomHandlerException(AwesomeVersionException):
    """Thrown when the custom handler is not configured properly."""
