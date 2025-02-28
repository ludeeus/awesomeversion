"""Constructor benchmarks for AwesomeVersion."""

from __future__ import annotations

from typing import Any

import pytest

from awesomeversion import AwesomeVersion, AwesomeVersionStrategy


@pytest.mark.benchmark
@pytest.mark.parametrize(
    "version,constructor_kv",
    [
        ["9999", {}],
        ["v1.2.3", {}],
        [
            "lorem_ipsum1.2.3",
            {
                "ensure_strategy": AwesomeVersionStrategy.SEMVER,
                "find_first_match": True,
            },
        ],
        ["dev", {}],
    ],
)
def test_constructor(version: str, constructor_kv: dict[str, Any]) -> None:
    """Benchmark for AwesomeVersion constructor."""
    assert AwesomeVersion(version, **constructor_kv)
