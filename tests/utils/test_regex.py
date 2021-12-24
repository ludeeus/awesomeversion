"""Test utils."""
import re
from typing import Union

import pytest

from awesomeversion.utils.regex import get_regex_match_group


@pytest.mark.parametrize(
    "pattern,string,index,result",
    (
        (r"\d+", "123", 0, "123"),
        (r"\d+", "123", 1, None),
        (r"\D+", "123", 1, None),
        (r"\D+", "123", 0, None),
    ),
)
def test_get_regex_match_group(
    pattern: str, string: str, index: int, result: Union[str, None]
) -> None:
    """Test get_regex_match_group."""
    assert get_regex_match_group(re.compile(pattern), string, index) == result
