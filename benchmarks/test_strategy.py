"""Strategy detection benchmarks for AwesomeVersion."""

from __future__ import annotations

import pytest
from pytest_codspeed import BenchmarkFixture

from awesomeversion import AwesomeVersion, AwesomeVersionStrategy

from .const import DEFAULT_RUNS


@pytest.mark.parametrize(
    "version",
    (
        "1.2.3",
        "1.2.3-alpha1",
        "1.2.3-beta.1",
        "1.2.3+build.1",
        "2020.12.1",
        "2020.12",
        "20.12.1",
        "1.2.3.dev0",
        "1.2.3a1",
        "1.2.3b2",
        "1.2.3rc1",
        "123",
        "999",
        "0x1a2b",
        "0xdeadbeef",
        "latest",
        "dev",
        "stable",
        "beta",
        "1.2",
        "1.2.3.4",
        "v1.2.3",
        "lorem_ipsum1.2.3",
        "prefix-1.2.3-suffix",
    ),
)
def test_strategy_detection(
    benchmark: BenchmarkFixture,
    version: str,
) -> None:
    """Benchmark for AwesomeVersion strategy detection."""

    @benchmark
    def _run_benchmark() -> None:
        for _ in range(DEFAULT_RUNS):
            obj = AwesomeVersion(version)
            obj.strategy


@pytest.mark.parametrize(
    "version,strategy",
    (
        ("lorem_ipsum1.2.3", AwesomeVersionStrategy.SEMVER),
        ("prefix-2020.12.1-suffix", AwesomeVersionStrategy.CALVER),
        ("text1.2.3.4text", AwesomeVersionStrategy.SIMPLEVER),
    ),
)
def test_find_first_match_strategy(
    benchmark: BenchmarkFixture,
    version: str,
    strategy: AwesomeVersionStrategy,
) -> None:
    """Benchmark for AwesomeVersion with find_first_match enabled."""

    @benchmark
    def _run_benchmark() -> None:
        for _ in range(DEFAULT_RUNS):
            AwesomeVersion(
                version,
                ensure_strategy=strategy,
                find_first_match=True,
            )


@pytest.mark.parametrize(
    "version,strategies",
    (
        ("1.2.3", [AwesomeVersionStrategy.SEMVER]),
        ("2020.12.1", [AwesomeVersionStrategy.CALVER, AwesomeVersionStrategy.SIMPLEVER]),
        ("999", [AwesomeVersionStrategy.BUILDVER]),
        ("1.2.3", [AwesomeVersionStrategy.SEMVER, AwesomeVersionStrategy.PEP440]),
    ),
)
def test_ensure_strategy_validation(
    benchmark: BenchmarkFixture,
    version: str,
    strategies: list[AwesomeVersionStrategy],
) -> None:
    """Benchmark for AwesomeVersion with ensure_strategy validation."""

    @benchmark
    def _run_benchmark() -> None:
        for _ in range(DEFAULT_RUNS):
            AwesomeVersion(version, ensure_strategy=strategies)
