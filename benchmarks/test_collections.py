"""Sorting and collection benchmarks for AwesomeVersion."""

from __future__ import annotations

import pytest
from pytest_codspeed import BenchmarkFixture

from awesomeversion import AwesomeVersion

from .const import DEFAULT_RUNS


SEMVER_VERSIONS = [
    "1.0.0",
    "1.0.1",
    "1.1.0",
    "1.1.1",
    "1.2.0",
    "2.0.0",
    "2.0.0-alpha",
    "2.0.0-alpha.1",
    "2.0.0-beta",
    "2.0.0-rc.1",
    "2.1.0",
    "10.0.0",
]

CALVER_VERSIONS = [
    "2020.1.1",
    "2020.2.1",
    "2020.12.1",
    "2021.1.1",
    "2021.6.15",
    "2021.12.25",
    "2022.1.1",
    "2022.3.14",
    "2023.1.1",
]

MIXED_VERSIONS = [
    "1.0.0",
    "2020.12.1",
    "999",
    "1.2.3-beta1",
    "2021.1.1",
    "1000",
    "1.2.4",
    "2020.6.15",
]


@pytest.mark.parametrize(
    "version_list",
    (
        pytest.param(SEMVER_VERSIONS, id="semver_versions"),
        pytest.param(CALVER_VERSIONS, id="calver_versions"),
        pytest.param(MIXED_VERSIONS, id="mixed_versions"),
    ),
)
def test_version_sorting(
    benchmark: BenchmarkFixture,
    version_list: list[str],
) -> None:
    """Benchmark for sorting lists of AwesomeVersion objects."""
    awesome_versions = [AwesomeVersion(v) for v in version_list]

    @benchmark
    def _run_benchmark() -> None:
        for _ in range(DEFAULT_RUNS):
            sorted(awesome_versions)


@pytest.mark.parametrize(
    "version_list",
    (
        pytest.param(SEMVER_VERSIONS, id="semver_versions"),
        pytest.param(CALVER_VERSIONS, id="calver_versions"),
        pytest.param(MIXED_VERSIONS, id="mixed_versions"),
    ),
)
def test_version_set_operations(
    benchmark: BenchmarkFixture,
    version_list: list[str],
) -> None:
    """Benchmark for set operations with AwesomeVersion objects."""
    awesome_versions = [AwesomeVersion(v) for v in version_list]
    duplicated_versions = awesome_versions + awesome_versions

    @benchmark
    def _run_benchmark() -> None:
        for _ in range(DEFAULT_RUNS):
            version_set = set(duplicated_versions)
            awesome_versions[0] in version_set
            version_set | {awesome_versions[1]}


@pytest.mark.parametrize(
    "version_list",
    (
        pytest.param(SEMVER_VERSIONS, id="semver_versions"),
        pytest.param(CALVER_VERSIONS, id="calver_versions"),
    ),
)
def test_version_list_creation(
    benchmark: BenchmarkFixture,
    version_list: list[str],
) -> None:
    """Benchmark for creating lists of AwesomeVersion objects."""

    @benchmark
    def _run_benchmark() -> None:
        for _ in range(DEFAULT_RUNS):
            [AwesomeVersion(v) for v in version_list]


def test_version_min_max_operations(
    benchmark: BenchmarkFixture,
) -> None:
    """Benchmark for min/max operations on version lists."""
    awesome_versions = [AwesomeVersion(v) for v in SEMVER_VERSIONS]

    @benchmark
    def _run_benchmark() -> None:
        for _ in range(DEFAULT_RUNS):
            min(awesome_versions)
            max(awesome_versions)
