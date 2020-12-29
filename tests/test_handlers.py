"""Test container handler."""
from awesomeversion import AwesomeVersion
from awesomeversion.handlers import CompareHandlers


def test_container():
    handlers = CompareHandlers(AwesomeVersion("latest"), AwesomeVersion("stable"))
    assert handlers.check()

    handlers = CompareHandlers(AwesomeVersion("latest"), AwesomeVersion("1"))
    assert handlers.check()

    handlers = CompareHandlers(AwesomeVersion("1.0.0"), AwesomeVersion("stable"))
    assert not handlers.check()


def test_dev():
    handlers = CompareHandlers(AwesomeVersion("1.dev1"), AwesomeVersion("1.dev0"))
    assert handlers.check()

    handlers = CompareHandlers(AwesomeVersion("1.dev0"), AwesomeVersion("1.dev1"))
    assert not handlers.check()


def test_modifier():
    handlers = CompareHandlers(AwesomeVersion("1.0b1"), AwesomeVersion("1.0b0"))
    assert handlers.check()

    handlers = CompareHandlers(AwesomeVersion("1.0"), AwesomeVersion("1.0b0"))
    assert handlers.check()

    handlers = CompareHandlers(AwesomeVersion("1.0b0"), AwesomeVersion("1.0b1"))
    assert not handlers.check()

    handlers = CompareHandlers(AwesomeVersion("1.0b0"), AwesomeVersion("1.0"))
    assert not handlers.check()


def test_sectons():
    handlers = CompareHandlers(AwesomeVersion("1.2.3.4.5b0"), AwesomeVersion("1.2b0"))
    assert handlers.check()


def test_simple():
    handlers = CompareHandlers(AwesomeVersion("2"), AwesomeVersion("1"))
    assert handlers.check()

    handlers = CompareHandlers(AwesomeVersion("1"), AwesomeVersion("2"))
    assert not handlers.check()
