# AwesomeVersion

[![codecov](https://codecov.io/gh/ludeeus/awesomeversion/branch/main/graph/badge.svg)](https://codecov.io/gh/ludeeus/awesomeversion)
![python version](https://img.shields.io/badge/Python-3.9=><=3.13-blue.svg)
![dependencies](https://img.shields.io/badge/Dependencies-0-blue.svg)
[![PyPI](https://img.shields.io/pypi/v/awesomeversion)](https://pypi.org/project/awesomeversion)
![Actions](https://github.com/ludeeus/awesomeversion/workflows/Actions/badge.svg?branch=main)

_One version package to rule them all, One version package to find them, One version package to bring them all, and in the darkness bind them._

Make anything a version object, and compare against a vast section of other version formats.

## Installation

```bash
python3 -m pip install awesomeversion
```


## Development

> **Note**
> 
> Development is only supported inside the provided devcontainer (such as GitHub Codespaces or VS Code Remote - Containers). Other local or system Python environments are not supported for development or contribution. All scripts and workflows assume the devcontainer environment.

This project uses the ["Scripts to Rule Them All"](https://github.blog/engineering/scripts-to-rule-them-all/) pattern for development tasks:

```bash
# Set up the project for development
./script/setup

# Run tests
./script/test

# Run linting and formatting
./script/lint

# Run coverage
./script/coverage
```

When using the devcontainer or GitHub Codespaces, a welcome message with available scripts is automatically displayed on startup.

## AwesomeVersion class

The AwesomeVersion class takes a version as the first argument, you can also pass in additional kwargs to customize the version object.

Argument | Description
--- | ---
`version` | The version string to parse.
`ensure_strategy` | Match the `AwesomeVersion` object against spesific strategies when creating if. If it does not match `AwesomeVersionStrategyException` will be raised
`find_first_match` | If True, the version given will be scanned for the first match of the given `ensure_strategy`. Raises `AwesomeVersionStrategyException` If it is not found for any of the given strategies.

## AwesomeVersion methods

<details>
<summary><code>AwesomeVersion.in_range</code></summary>

This is a helper method to check if the version is in a range.
This method takes two arguments, `lowest` and `highest`, both are required, and returns a boolean.

> **Note** This method is the same as doing `lowest <= AwesomeVersion <= highest`

Example:

```python
from awesomeversion import AwesomeVersion
print(AwesomeVersion("1.2.2").in_range("1.2.1", "1.3"))
> True
print(AwesomeVersion("1.2.0").in_range("1.2.1", "1.3"))
> False
```

</details>

<details>
<summary><code>AwesomeVersion.diff</code></summary>

This is a helper method to get the difference between two versions.
This method takes one argument which is the version to compare against, and returns a `AwesomeVersionDiff` object.

> **Note** This method is the same as doing `AwesomeVersion - version`

Example:

```python
from awesomeversion import AwesomeVersion
> print(AwesomeVersion("1.0").diff("2.1"))
AwesomeVersionDiff(major=True, minor=True, patch=False, modifier=False, strategy=False)
```

</details>


<details>
<summary><code>AwesomeVersion.section</code></summary>

This is a helper method to get a section of the version.
This method takes one argument which is the section to get, and returns an integer representing it (or 0 if it does not exist).

Example:

```python
from awesomeversion import AwesomeVersion
> print(AwesomeVersion("1.0").section(0))
1
```

</details>


## AwesomeVersion properties

Argument | Description
--- | ---
`alpha` | This is a boolean representing if the version is an alpha version.
`beta` | This is a boolean representing if the version is a beta version.
`dev` | This is a boolean representing if the version is a dev version.
`major` | This is an `AwesomeVersion` object representing the major version or `None` if not present.
`micro` | This is an `AwesomeVersion` object representing the micro version or `None` if not present.
`minor` | This is an `AwesomeVersion` object representing the minor version or `None` if not present.
`modifier_type` | This is a string representing the modifier type of the version or `None` if not present.
`modifier` | This is a string representing the modifier of the version or `None` if not present.
`patch` | This is an `AwesomeVersion` object representing the patch version or `None` if not present.
`prefix` | This is the prefix of the version or `None` if not present.
`release_candidate` | This is a boolean representing if the version is a release candidate version.
`simple` | This is a boolean representing if the version is a simple version.
`strategy_description` | This is a `AwesomeVersionStrategyDescription` object representing the strategy description of the version.
`strategy` | This is a `AwesomeVersionStrategy` object representing the strategy of the version.
`string` | This is the string representation of the version (without the v prefix if present).
`valid` | This is a boolean representing if the version is valid (not unknown strategy).
`year` | This is alias to `major`, and is an `AwesomeVersion` object representing the year.


## Example usage

Here are some examples of how you can use this package, more examples can be found in the `tests` directory.

<details>
<summary><code>Basic compare</code></summary>

```python
from awesomeversion import AwesomeVersion

current = AwesomeVersion("1.2.2")
upstream = AwesomeVersion("1.2.3")

print(upstream > current)
> True
```

</details>

<details>
<summary><code>Compare beta version</code></summary>

```python
from awesomeversion import AwesomeVersion

current = AwesomeVersion("2021.1.0")
upstream = AwesomeVersion("2021.1.0b2")

print(current > upstream)
> True
```

</details>

<details>
<summary><code>Check if version is a beta version</code></summary>

```python
from awesomeversion import AwesomeVersion

print(AwesomeVersion("1.2.3b0").beta)
> True

print(AwesomeVersion("1.2.3").beta)
> False
```

</details>

<details>
<summary>Use <code>AwesomeVersion</code> with <code>with ...</code></summary>

```python
from awesomeversion import AwesomeVersion

with AwesomeVersion("20.12.0") as current:
    with AwesomeVersion("20.12.1") as upstream:
        print(upstream > current)
> True
```

</details>

<details>
<summary>Compare <code>AwesomeVersion</code> with other non-<code>AwesomeVersion</code> formats</summary>

```python
from awesomeversion import AwesomeVersion

base = AwesomeVersion("20.12.0")

print(base > "20.12.1")
> False

print(base > "19")
> True

print(base > 5)
> True
```

</details>


## General behavior

You can test your versions on the [demo page][awesomeversion_demo].

### Modifiers

When comparing versions with modifiers, if the base version is the same the modifier will be used to determine the order.
If one of the versions do not have a modifier, the one without will be considered newer.

The order of the modifiers are:
- No modifier
- RC
- Beta
- Alpha
- Dev

<details>
<summary>Examples</summary>

```python
from awesomeversion import AwesomeVersion

print(AwesomeVersion("1.0.0") > AwesomeVersion("1.0.0b6"))
> True
print(AwesomeVersion("1.0.0") > AwesomeVersion("1.0.0.dev6"))
> True
print(AwesomeVersion("1.0.0.dev19") > AwesomeVersion("1.0.0b4"))
> False
```

</details>


### Special versions (container)

There are some special versions for container that are handled differently than typical version formats.
The special versions are in the following order:
- `dev` (newest)
- `latest`
- `beta`
- `stable` (oldest)

If only the first version is this special version, it will be considered newer.
If only the second version is this special version, it will be considered older.


<details>
<summary>Examples</summary>

```python
from awesomeversion import AwesomeVersion

print(AwesomeVersion("latest") > AwesomeVersion("1.0.0b6"))
> True
print(AwesomeVersion("1.0.0") > AwesomeVersion("latest"))
> False
print(AwesomeVersion("stable") > AwesomeVersion("latest"))
> False
print(AwesomeVersion("beta") > AwesomeVersion("dev"))
> False
```

</details>




## Contribute

**All** contributions are welcome!

1. Fork the repository
2. Clone the repository locally and open the devcontainer or use GitHub codespaces
3. Do your changes
4. Lint the files with `script/lint`
5. Ensure all tests passes with `script/test`
6. Ensure 100% coverage with `script/coverage`
7. Commit your work, and push it to GitHub
8. Create a PR against the `main` branch


[awesomeversion_demo]: https://ludeeus.github.io/awesomeversion/