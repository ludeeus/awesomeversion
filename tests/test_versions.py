"""Test versions."""

from awesomeversion.strategy import AwesomeVersionStrategy

TEST_VERSIONS = [
    "",
    "0.1",
    "0.118.0",
    "0",
    "1.0.0-alpha.1",
    "1.0.0-alpha.2",
    "1.0.0-alpha",
    "1.0.0-alpha+1.2",
    "1.0.0-alpha1",
    "1.0.0-alpha10",
    "1.0.0-alpha9",
    "1.0.0-beta.1",
    "1.0.0-beta.10",
    "1.0.0-beta.2",
    "1.0.0-beta.9",
    "1.0.0-beta",
    "1.0.0-beta0",
    "1.0.0-beta1",
    "1.0.0-rc.1",
    "1.0.0-rc.2",
    "1.0.0-rc0",
    "1.0.0",
    "1.0.0b0",
    "1.0.0b1",
    "1.0.0b10",
    "1.0.0b9",
    "1.0.0beta0",
    "1.0.0rc0",
    "1.0.1",
    "1.0.a0",
    "1.0.alpha1",
    "1.0.b0",
    "1.0.b1",
    "1.0.b2",
    "1.0.d1",
    "1.0.dev0",
    "1.0.dev1",
    "1.0.dev456",
    "1.0.invalid4",
    "1.0.post456.dev34",
    "1.0.post456",
    "1.0.rc2",
    "1.0",
    "1.0+local.1.2.3",
    "1.0a1",
    "1.0a12.dev456",
    "1.0a12",
    "1.0a2.dev456",
    "1.0b0",
    "1.0b1.dev456",
    "1.0b1",
    "1.0b2.post345.dev456",
    "1.0b2.post345",
    "1.0b2",
    "1.0rc1.dev456",
    "1.0rc1",
    "1.0rc1+local.1.2.3",
    "1.1.dev1",
    "1.1-dev1",
    "1.1_dev1",
    "1.1",
    "1.2.3-1",
    "1.2.3-2",
    "1.2.3-alpha.1",
    "1.2.3-dev.1",
    "1.2.3.4.5.6.6.8",
    "1.2.3.4.5.6.7.8.9",
    "1.2.3.4.5.6.7.8",
    "1.2.3.4.5",
    "1.2.3.4.5b0",
    "1.2.3.4",
    "1.2.3",
    "1.2b0",
    "1.8.2-beta.1.10",
    "1.8.2-beta.1.10+somebuild",
    "1.8.2-beta.1.13",
    "1.dev0",
    "1.dev1",
    "1-dev1",
    "1_dev1",
    "1",
    "123",
    "2.0.0-alpha.1",
    "2.0.0-alpha.2",
    "2.0.0-beta.1",
    "2.0.0-beta.2",
    "2.0.0-rc.1",
    "2.0.0-rc.2",
    "2.0.0",
    "2.1.0",
    "2.1.1",
    "2.1.3",
    "2.4.6-8",
    "2",
    "20.1.0",
    "20.1",
    "2019",
    "2020.1.1.",
    "2020.1",
    "2020.12.0",
    "2020.12.1",
    "2020.12.dev1602",
    "2020.12.dev1603",
    "2020.2.0",
    "2020.21.1",
    "2020",
    "2021.1.0.0",
    "2021.1.0.dev0",
    "2021.1.0",
    "2021.1.0a0",
    "2021.1.0b0",
    "2021.1.0b1",
    "2021.1.0b2",
    "2021.1.0dev0",
    "2021.1.0dev20210101",
    "2021.2.0.dev20210118",
    "2021.2.0",
    "2021.2.0b0",
    "2021.2.0b10",
    "2022.01.01",
    "2022.01.02",
    "2022.02.01",
    "2022.02.02",
    "2022.03.01",
    "2022.03.02",
    "2023.01.01",
    "2023.01.02",
    "2023.02.01",
    "2023.02.02",
    "2023.03.01",
    "2023.03.02",
    "3.0.0-alpha.1",
    "3.0.0-alpha.2",
    "3.0.0-beta.1",
    "3.0.0-beta.2",
    "3.0.0-rc.1",
    "3.0.0-rc.2",
    "3.0.0",
    "3.0.1",
    "4.0.0",
    "4.1.0",
    "4.2.0",
    "5.0.0",
    "5.1.0",
    "5.1.1",
    "5.10",
    "5.11",
    "6.0.0",
    "6.0.dev20210429",
    "6.0.rc1",
    "6.0",
    "6.1.0",
    "6.2.0",
    "7.0.0",
    "7.1.0",
    "7.1.1",
    "a.b.c",
    "beta",
    "dev",
    "latest",
    "stable",
    "unknown",
    "v1.0.1",
    "v1.0",
    "v1.1.1",
    "v1.1",
    "v1.2.1",
    "v1.2",
    "v2.0.1",
    "v2.0",
    "v2.1.1",
    "v2.1",
    "v2.2.1",
    "v2.2",
    "00AABB00",
    "01234567",
    "0x0",
    "0x01002100",
    0x01002101,
    "0X01002604",
    "0x2df35",
    "0x00AABB00",
    "0x23089631",
    "0x0g",
    AwesomeVersionStrategy,
    False,
    None,
    str,
    True,
]


def test_human_error_in_version_list() -> None:
    """Test for human error in version list."""
    assert len(TEST_VERSIONS) == len(set(TEST_VERSIONS))
