"""Compare benchmarks for AwesomeVersion."""

import pytest

from awesomeversion import AwesomeVersion

newer_older_cases = [
    ["9999", "1"],
    ["9999", "2020.1.1"],
    ["1.2.3b6", "1.2.3.dev4"],
]


@pytest.mark.benchmark
@pytest.mark.parametrize("a,b", newer_older_cases)
def test_newer(a: str, b: str) -> None:
    """Benchmark for AwesomeVersion comparison."""
    assert AwesomeVersion(a) > b


@pytest.mark.benchmark
@pytest.mark.parametrize("a,b", ([x[1], x[0]] for x in newer_older_cases))
def test_older(a: str, b: str) -> None:
    """Benchmark for AwesomeVersion comparison."""
    assert AwesomeVersion(a) < b


@pytest.mark.benchmark
@pytest.mark.parametrize(
    "version",
    [
        "1.2.3",
        "v1.2.3'",
        "v1.2.3",
        "1.2.3.dev4",
        "1.2.3b6",
        "1.2.3.post4",
        "1.2.3.post4.dev6",
        "1.2.3.post4.dev6+githash",
        1,
        3.14,
    ],
)
def test_equal(version: str) -> None:
    """Benchmark for AwesomeVersion comparison."""
    assert AwesomeVersion(version) == version
