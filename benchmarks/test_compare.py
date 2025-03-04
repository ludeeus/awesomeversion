"""Compare benchmarks for AwesomeVersion."""

import pytest
from pytest_codspeed import BenchmarkFixture

from awesomeversion import AwesomeVersion


@pytest.mark.benchmark
@pytest.mark.parametrize(
    "input_a,operator, input_b",
    (
        pytest.param("9999", ">", "1", id="9999>1"),
        pytest.param("9999", ">", "2020.1.1", id="9999>2020.1.1"),
        pytest.param("1.2.3b6", ">", "1.2.3.dev4", id="1.2.3b6>1.2.3.dev4"),
        pytest.param("1.2.3", "==", "1.2.3", id="1.2.3==1.2.3"),
        pytest.param("1.2.3", "!=", "3.2.1", id="1.2.3!=3.2.1"),
    ),
)
def test_compare(
    benchmark: BenchmarkFixture, input_a: str, operator: str, input_b: str
) -> None:
    """Benchmark for AwesomeVersion comparison."""
    obj = AwesomeVersion(input_a)
    if operator == ">":

        @benchmark
        def _run_banchmark() -> None:
            for _ in range(100):
                assert obj > input_b

    elif operator == "<":

        @benchmark
        def _run_banchmark() -> None:
            for _ in range(100):
                assert obj < input_b

    elif operator == "==":

        @benchmark
        def _run_banchmark() -> None:
            for _ in range(100):
                assert obj == input_b

    elif operator == "!=":

        @benchmark
        def _run_banchmark() -> None:
            for _ in range(100):
                assert obj != input_b
