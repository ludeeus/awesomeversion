"""Operations benchmarks for AwesomeVersion."""

from __future__ import annotations

import pytest
from pytest_codspeed import BenchmarkFixture

from awesomeversion import AwesomeVersion

from .const import DEFAULT_RUNS


@pytest.mark.parametrize(
    "version",
    (
        "1.2.3",
        "2020.12.1",
        "v1.2.3-beta1",
        "1.2.3.dev4",
        "999",
        "0x1a2b",
        "latest",
    ),
)
def test_string_representation(
    benchmark: BenchmarkFixture,
    version: str,
) -> None:
    """Benchmark for AwesomeVersion string representation operations."""
    obj = AwesomeVersion(version)

    @benchmark
    def _run_benchmark() -> None:
        for _ in range(DEFAULT_RUNS):
            str(obj)
            repr(obj)


@pytest.mark.parametrize(
    "version",
    (
        "1.2.3",
        "2020.12.1",
        "v1.2.3-beta1",
        "1.2.3.dev4",
        "999",
        "0x1a2b",
        "latest",
    ),
)
def test_hash_operation(
    benchmark: BenchmarkFixture,
    version: str,
) -> None:
    """Benchmark for AwesomeVersion hash operations."""
    obj = AwesomeVersion(version)

    @benchmark
    def _run_benchmark() -> None:
        for _ in range(DEFAULT_RUNS):
            hash(obj)


@pytest.mark.parametrize(
    "version_a,version_b",
    (
        ("1.2.3", "1.2.4"),
        ("2020.12.1", "2021.12.1"),
        ("1.2.3-beta1", "1.2.3-beta2"),
        ("1.2.3", "1.3.0"),
        ("999", "1000"),
    ),
)
def test_diff_operation(
    benchmark: BenchmarkFixture,
    version_a: str,
    version_b: str,
) -> None:
    """Benchmark for AwesomeVersion diff operations."""
    obj_a = AwesomeVersion(version_a)

    @benchmark
    def _run_benchmark() -> None:
        for _ in range(DEFAULT_RUNS):
            obj_a.diff(version_b)


@pytest.mark.parametrize(
    "version,lowest,highest",
    (
        ("1.2.3", "1.0.0", "2.0.0"),
        ("2020.12.1", "2020.1.1", "2021.1.1"),
        ("15", "10", "20"),
        ("1.2.3-beta1", "1.2.2", "1.2.4"),
    ),
)
def test_in_range_operation(
    benchmark: BenchmarkFixture,
    version: str,
    lowest: str,
    highest: str,
) -> None:
    """Benchmark for AwesomeVersion in_range operations."""
    obj = AwesomeVersion(version)

    @benchmark
    def _run_benchmark() -> None:
        for _ in range(DEFAULT_RUNS):
            obj.in_range(lowest, highest)


@pytest.mark.parametrize(
    "version,section_idx",
    (
        ("1.2.3", 0),
        ("1.2.3", 1),
        ("1.2.3", 2),
        ("2020.12.1", 0),
        ("2020.12.1.4", 3),
    ),
)
def test_section_access(
    benchmark: BenchmarkFixture,
    version: str,
    section_idx: int,
) -> None:
    """Benchmark for AwesomeVersion section access."""
    obj = AwesomeVersion(version)

    @benchmark
    def _run_benchmark() -> None:
        for _ in range(DEFAULT_RUNS):
            obj.section(section_idx)


@pytest.mark.parametrize(
    "version",
    (
        "1.2.3-alpha1",
        "1.2.3-beta2",
        "1.2.3-dev3",
        "1.2.3-rc1",
        "1.2.3",
    ),
)
def test_boolean_properties(
    benchmark: BenchmarkFixture,
    version: str,
) -> None:
    """Benchmark for AwesomeVersion boolean properties."""
    obj = AwesomeVersion(version)

    @benchmark
    def _run_benchmark() -> None:
        for _ in range(DEFAULT_RUNS):
            _ = obj.alpha
            _ = obj.beta
            _ = obj.dev
            _ = obj.release_candidate
            _ = obj.valid
