"""Constructor benchmarks for AwesomeVersion."""

from __future__ import annotations

from typing import Any

import pytest

from awesomeversion import AwesomeVersion, AwesomeVersionStrategy

semver_first = {
    "ensure_strategy": AwesomeVersionStrategy.SEMVER,
    "find_first_match": True,
}


@pytest.mark.benchmark
@pytest.mark.parametrize(
    "version,constructor_kv",
    [
        pytest.param("9999", {}, id="9999-default"),
        pytest.param("v1.2.3", {}, id="v1.2.3-default"),
        pytest.param(
            "lorem_ipsum1.2.3",
            semver_first,
            id="lorem_ipsum1.2.3-semver-first",
        ),
        pytest.param("dev", {}, id="dev-default"),
        pytest.param(1, {}, id="1-as-int-default"),
        pytest.param("1", {}, id="1-as-str-default"),
        pytest.param(3.14, {}, id="3.14-as-float-default"),
        pytest.param(
            "1.2.3",
            semver_first,
            id="1.2.3-semver-first",
        ),
    ],
)
def test_constructor(
    version: str | int | float, constructor_kv: dict[str, Any]
) -> None:
    """Benchmark for AwesomeVersion constructor."""
    for _ in range(100):
        assert AwesomeVersion(version, **constructor_kv)
