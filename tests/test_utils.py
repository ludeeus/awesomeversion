"""Test utils."""
import re

from awesomeversion.utils import get_regex_match_group


def test_get_regex_match_group():
    """Test get_regex_match_group."""
    assert get_regex_match_group(re.compile(r"\d+"), "123", 0) == "123"
    assert get_regex_match_group(re.compile(r"\d+"), "123", 1) is None
    assert get_regex_match_group(re.compile(r"\D+"), "123", 0) is None
