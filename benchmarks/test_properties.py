"""Property benchmarks for AwesomeVersion."""

from __future__ import annotations

import pytest
from pytest_codspeed import BenchmarkFixture

from awesomeversion import AwesomeVersion, AwesomeVersionStrategy

from .const import DEFAULT_RUNS

semver_first = {
    "ensure_strategy": AwesomeVersionStrategy.SEMVER,
    "find_first_match": True,
}


@pytest.mark.parametrize(
    "version,class_property",
    (
        *[(version, "prefix") for version in ("v1.2.3", "v.1.2.3", "1.2.3")],
        *[(version, "modifier") for version in ("1.2.3-dev2", "1.2.3dev2")],
        *[(version, "modifier_type") for version in ("1.2.3.dev0", "1.2.3.beta0")],
        *[(version, "strategy") for version in ("1.2.3", "2099.1.1", "999")],
        *[
            (version, "strategy_description")
            for version in ("1.2.3", "2099.1.1", "999")
        ],
        *[
            (version, segment)
            for version in ("1.2.3", "123", "0.1.2.3")
            for segment in ("major", "minor", "patch")
        ],
    ),
)
def test_property(
    benchmark: BenchmarkFixture,
    version: str | int | float,
    class_property: str,
) -> None:
    """Benchmark for AwesomeVersion properties."""
    obj = AwesomeVersion(version)

    @benchmark
    def _run_banchmark() -> None:
        for _ in range(DEFAULT_RUNS):
            getattr(obj, class_property)
