"""Test container handler."""
from awesomeversion import AwesomeVersion
from awesomeversion.handlers import CompareHandlers


def test_container():
    handler = CompareHandlers(AwesomeVersion("latest"), AwesomeVersion("stable"))
    assert handler.check()

    handler = CompareHandlers(AwesomeVersion("latest"), AwesomeVersion("1"))
    assert handler.check()

    handler = CompareHandlers(AwesomeVersion("1.0.0"), AwesomeVersion("stable"))
    assert not handler.check()


def test_dev():
    handler = CompareHandlers(AwesomeVersion("1.dev1"), AwesomeVersion("1.dev0"))
    assert handler.check()

    handler = CompareHandlers(AwesomeVersion("1.dev0"), AwesomeVersion("1.dev1"))
    assert not handler.check()


def test_modifier():
    handler = CompareHandlers(AwesomeVersion("1.0b1"), AwesomeVersion("1.0b0"))
    assert handler.check()

    handler = CompareHandlers(AwesomeVersion("1.0"), AwesomeVersion("1.0b0"))
    assert handler.check()

    handler = CompareHandlers(AwesomeVersion("1.0b0"), AwesomeVersion("1.0b1"))
    assert not handler.check()

    handler = CompareHandlers(AwesomeVersion("1.0b0"), AwesomeVersion("1.0"))
    assert not handler.check()


def test_sectons():
    handler = CompareHandlers(AwesomeVersion("1.2.3.4.5b0"), AwesomeVersion("1.2b0"))
    assert handler.check()


def test_simple():
    handler = CompareHandlers(AwesomeVersion("2"), AwesomeVersion("1"))
    assert handler.check()

    handler = CompareHandlers(AwesomeVersion("1"), AwesomeVersion("2"))
    assert not handler.check()

    handler = CompareHandlers(AwesomeVersion("1"), AwesomeVersion("1"))
    assert not handler.check()

    handler = CompareHandlers(AwesomeVersion("1.0"), AwesomeVersion("1.0"))
    assert not handler.check()

    handler = CompareHandlers(AwesomeVersion("5.10"), AwesomeVersion("5.10"))
    assert not handler.check()
