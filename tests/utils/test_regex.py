"""Test utils."""
import re

import pytest

from awesomeversion.utils.regex import (
    get_regex_match,
    get_regex_match_group,
    is_regex_matching,
)


@pytest.mark.parametrize(
    "pattern,string,index,result",
    (
        (r"\d+", "123", 0, "123"),
        (r"\d+", "123", 1, None),
        (r"\D+", "123", 1, None),
        (r"\D+", "123", None, None),
    ),
)
def test_get_regex_match_group(pattern, string, index, result):
    """Test get_regex_match_group."""
    assert get_regex_match_group(re.compile(pattern), string, index) == result


@pytest.mark.parametrize(
    "pattern,string,result",
    ((r"\d+", "123", True), (r"\d+", 123, True), (r"\D+", "123", False)),
)
def test_is_regex_matching(pattern, string, result):
    """Test is_regex_matching."""
    if result:
        assert is_regex_matching(re.compile(pattern), string)
    else:
        assert not is_regex_matching(re.compile(pattern), string)


@pytest.mark.parametrize(
    "pattern,string,result",
    ((r"\d+", "123", True), (r"\d+", 123, True), (r"\D+", "123", False)),
)
def test_get_regex_match(pattern, string, result):
    """Test get_regex_match."""
    if result:
        assert get_regex_match(re.compile(pattern), string) is not None
    else:
        assert get_regex_match(re.compile(pattern), string) is None
