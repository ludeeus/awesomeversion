"""Testing with snapshots."""
import json

import pytest
from pytest_snapshot.plugin import Snapshot  # type: ignore

from awesomeversion import AwesomeVersion
from awesomeversion.typing import VersionType

from .test_versions import TEST_VERSIONS


@pytest.mark.parametrize("version", TEST_VERSIONS)
def test_awesomeversion_output_with_snapshot(
    version: VersionType,
    snapshot: Snapshot,
) -> None:
    """Test AwesomeVersion output with snapshot."""
    version_obj = AwesomeVersion(version)

    snapshot.snapshot_dir = f"tests/snapshots/{version_obj.strategy.value}"
    snapshot.assert_match(
        json.dumps(
            {
                key: getattr(version_obj, key)
                for key in [
                    "alpha",
                    "beta",
                    "dev",
                    "major",
                    "micro",
                    "minor",
                    "modifier_type",
                    "modifier",
                    "patch",
                    "prefix",
                    "release_candidate",
                    "sections",
                    "simple",
                    "strategy",
                    "string",
                    "valid",
                    "year",
                ]
            },
            indent=4,
        ),
        f"{version}.json",
    )
