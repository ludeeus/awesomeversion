# AwesomeVersion

[![codecov](https://codecov.io/gh/ludeeus/awesomeversion/branch/main/graph/badge.svg)](https://codecov.io/gh/ludeeus/awesomeversion)
![python version](https://img.shields.io/badge/Python-3.7=><=3.10-blue.svg)
![dependencies](https://img.shields.io/badge/Dependencies-0-blue.svg)
[![PyPI](https://img.shields.io/pypi/v/awesomeversion)](https://pypi.org/project/awesomeversion)
![Actions](https://github.com/ludeeus/awesomeversion/workflows/Actions/badge.svg?branch=main)

_One version package to rule them all, One version package to find them, One version package to bring them all, and in the darkness bind them._

Make anything a version object, and compare against a vast section of other version formats.

## Installation

```bash
python3 -m pip install awesomeversion
```

## AwesomeVersion class

The AwesomeVersion class takes a version as the first argument, you can also pass in additional kwargs to customize the version object.

Argument | Description
--- | ---
`version` | The version string to parse.
`ensure_strategy` | Match the `AwesomeVersion` object against spesific strategies when creating if. If it does not match `AwesomeVersionStrategyException` will be raised
`find_first_match` | If True, the version given will be scanned for the first match of the given `ensure_strategy`. Raises `AwesomeVersionStrategyException` If it is not found for any of the given strategies.


## Example usage

These are some examples of what you can do, more examples can be found in the `tests` directory.

```python
from awesomeversion import AwesomeVersion

current = AwesomeVersion("1.2.2")
upstream = AwesomeVersion("1.2.3")

print(upstream > current)
> True
```

```python
from awesomeversion import AwesomeVersion

version = AwesomeVersion("1.2.3b0")

print(version.beta)
> True
```

```python
from awesomeversion import AwesomeVersion

current = AwesomeVersion("2021.1.0")
upstream = AwesomeVersion("2021.1.0b2")

print(upstream > current)
> False
```

```python
from awesomeversion import AwesomeVersion

current = AwesomeVersion("latest")
upstream = AwesomeVersion("2021.1.0")

print(upstream > current)
> False
```

```python
from awesomeversion import AwesomeVersion

current = AwesomeVersion("latest")
upstream = AwesomeVersion("dev")

print(upstream > current)
> True
```

```python
from awesomeversion import AwesomeVersion

with AwesomeVersion("20.12.0") as current:
    with AwesomeVersion("20.12.1") as upstream:
        print(upstream > current)
> True
```

```python
from awesomeversion import AwesomeVersion

with AwesomeVersion("20.12.0") as current:
    print("2020.12.1" > current)
> True
```

```python
from awesomeversion import AwesomeVersion

version = AwesomeVersion("2.12.0")
print(version.major)
> 2
print(version.minor)
> 12
print(version.patch)
> 0
```

## Contribute

**All** contributions are welcome!

1. Fork the repository
2. Clone the repository locally and open the devcontainer or use GitHub codespaces
3. Do your changes
4. Lint the files with `make lint`
5. Ensure all tests passes with `make test`
6. Ensure 100% coverage with `make coverage`
7. Commit your work, and push it to GitHub
8. Create a PR against the `main` branch
