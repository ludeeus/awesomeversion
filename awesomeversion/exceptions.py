"""Exceptions for AwesomeVersion."""


class AwesomeVersionException(Exception):
    """Base AwesomeVersion exception."""


class AwesomeVersionCompare(AwesomeVersionException):
    """Thrown when compare is not possible."""


class AwesomeVersionStrategyException(AwesomeVersionException):
    """Thrown when the expecte strategy does not match."""


class AwesomeVersionNotImplementedError(AwesomeVersionException, NotImplementedError):
    """Thrown when a method is not implemented."""
