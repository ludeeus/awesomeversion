"""Edge cases and complex parsing benchmarks for AwesomeVersion."""

from __future__ import annotations

import pytest
from pytest_codspeed import BenchmarkFixture

from awesomeversion import AwesomeVersion

from .const import DEFAULT_RUNS

COMPLEX_VERSIONS = [
    "1.0.post456.dev34",
    "1.0a12.dev456",
    "1.0b2.post345.dev456",
    "1.0rc1+local.1.2.3",
    "2021.2.0.dev20210118",
    "2021.1.0dev20210101",
    "1.0.0-alpha.1+build.123.456",
    "1.8.2-beta.1.10+somebuild",
    "1.0.0-alpha+1.2",
    "1.2.3.4.5.6.7.8.9",
    "1.2.3.4.5.6.6.8",
    "v1.2.3-alpha.1",
    "V.1.2.3-beta",
    "2020.1.1.",
    "1.1-dev1",
    "1.1_dev1",
    "1-dev1",
    "1_dev1",
    "0",
    "",
    "0.0.0",
    "latest",
    "dev",
    "stable",
    "beta",
    "0xdeadbeef",
    "0x1a2b3c4d",
    "123456789123456789123456789123456789123456789123456789123456789",
    "999999999999999999999999999999999999999999999999999999999999999",
]


@pytest.mark.parametrize(
    "version",
    COMPLEX_VERSIONS,
)
def test_complex_version_parsing(
    benchmark: BenchmarkFixture,
    version: str,
) -> None:
    """Benchmark for parsing complex version strings."""

    @benchmark
    def _run_benchmark() -> None:
        for _ in range(DEFAULT_RUNS):
            AwesomeVersion(version)


@pytest.mark.parametrize(
    "version",
    [
        "1.0.0-alpha.1",
        "1.0.post456.dev34",
        "1.8.2-beta.1.10+somebuild",
        "2021.1.0dev20210101",
        "1.2.3.4.5b0",
    ],
)
def test_modifier_parsing(
    benchmark: BenchmarkFixture,
    version: str,
) -> None:
    """Benchmark for parsing version modifiers."""
    obj = AwesomeVersion(version)

    @benchmark
    def _run_benchmark() -> None:
        for _ in range(DEFAULT_RUNS):
            obj.modifier
            obj.modifier_type


@pytest.mark.parametrize(
    "version",
    [
        "v1.2.3",
        "V.1.2.3-beta",
        "v1.0.0-alpha.1",
        "V1.0.post456",
    ],
)
def test_prefix_handling(
    benchmark: BenchmarkFixture,
    version: str,
) -> None:
    """Benchmark for handling version prefixes."""
    obj = AwesomeVersion(version)

    @benchmark
    def _run_benchmark() -> None:
        for _ in range(DEFAULT_RUNS):
            obj.prefix
            obj.string


@pytest.mark.parametrize(
    "version",
    [
        "1.2.3.4.5.6.7.8.9",
        "1.2.3.4.5.6.6.8",
        "1.2.3.4.5",
        "2021.1.0.0",
    ],
)
def test_multi_section_versions(
    benchmark: BenchmarkFixture,
    version: str,
) -> None:
    """Benchmark for versions with many sections."""
    obj = AwesomeVersion(version)

    @benchmark
    def _run_benchmark() -> None:
        for _ in range(DEFAULT_RUNS):
            obj.sections
            obj.major
            obj.minor
            obj.patch


def test_version_nesting_performance(
    benchmark: BenchmarkFixture,
) -> None:
    """Benchmark for creating AwesomeVersion from AwesomeVersion."""
    base_version = AwesomeVersion("1.2.3")

    @benchmark
    def _run_benchmark() -> None:
        for _ in range(DEFAULT_RUNS):
            AwesomeVersion(base_version)


@pytest.mark.parametrize(
    "version_input",
    [
        1,
        123,
        3.14,
        0,
        999999999,
    ],
)
def test_non_string_inputs(
    benchmark: BenchmarkFixture,
    version_input: int | float,
) -> None:
    """Benchmark for non-string version inputs."""

    @benchmark
    def _run_benchmark() -> None:
        for _ in range(DEFAULT_RUNS):
            AwesomeVersion(version_input)
