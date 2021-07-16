# AwesomeVersion

[![codecov](https://codecov.io/gh/ludeeus/awesomeversion/branch/main/graph/badge.svg)](https://codecov.io/gh/ludeeus/awesomeversion)
![python version](https://img.shields.io/badge/Python-3.6=><=3.10-blue.svg)
![dependencies](https://img.shields.io/badge/Dependencies-0-blue.svg)
[![PyPI](https://img.shields.io/pypi/v/awesomeversion)](https://pypi.org/project/awesomeversion)
![Actions](https://github.com/ludeeus/awesomeversion/workflows/Actions/badge.svg?branch=main)

_One version package to rule them all, One version package to find them, One version package to bring them all, and in the darkness bind them._

Make anything a version object, and compare against a vast section of other version formats.

## Installation

```bash
python3 -m pip install awesomeversion
```

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

## Customize the behaviour

You can add custom strategies and custom handlers to better suite your needs.

### Custom strategies

If you need to add a custom strategy to the `AwesomeVersion` object, you can do that creating a custom subclass of `AwesomeVersionStrategyBase` and passing that to the `AwesomeVersion` constructor with the `custom_strategies` argument.

Example:

```python
from re import compile
from awesomeversion import AwesomeVersion, AwesomeVersionStrategyBase

class MyAwesomeStrategy(AwesomeVersionStrategyBase):

    STRATEGY = "AwesomeVer"
    REGEX_MATCH = compile(r"awesome")

    def match(self) -> bool:
        """Return true if the version matches this strategy."""
        return self.version == "awesome"

assert AwesomeVersion("awesome", custom_strategies=[MyAwesomeStrategy]).strategy == "AwesomeVer"
```

- Custom strategies are checked before the built-in strategies.
- The `MyAwesomeStrategy.STRATEGY` defaults to `Custom`
- You only need one of `REGEX_MATCH`, `MyAwesomeStrategy.match`. `REGEX_MATCH` is prefered if both exist.
- Use `self.version` in `MyAwesomeStrategy.match` to access the version string.


### Custom handlers

If you need to add a custom strategy to the `AwesomeVersion` object, you can do that creating a custom subclass of `AwesomeVersionCompareHandler` and passing that to the `AwesomeVersion` constructor with the `custom_compare_handlers` argument.

Example:

```python
from awesomeversion import (
    AwesomeVersion,
    AwesomeVersionCompareHandler,
    AwesomeVersionStrategy,
)


class MyAwesomeHandler(AwesomeVersionCompareHandler):
    STRATEGIES = [AwesomeVersionStrategy.SEMVER]

    def handler(self) -> bool:
        """Custom compare handler."""
        print(self.version_a)
        if self.version_a == "1.2.3":
            return True


assert AwesomeVersion("1.2.3", custom_compare_handlers=[MyAwesomeHandler]) > "111.2.3"
```

- Custom compare handlers are checked before the built-in handlers.
- If `MyAwesomeHandler.STRATEGIES` is not defined, the default is `[]` which enables it for all strategies.
- `MyAwesomeHandler.handler` must return a boolean or `None`.
    - If `None` is returned it will check the next hadnler.
- Use `self.version_a` and `self.version_b` in `MyAwesomeHandler.handler` to access the `AwesomeVersion` objects.


## Contribute

**All** contributions are welcome!

1. Fork the repository
2. Clone the repository locally and open the devcontainer or use GitHub codespaces
3. Do your changes
4. Lint the files with `make black`
5. Ensure all tests passes with `make test`
6. Ensure 100% coverage with `make coverage`
7. Commit your work, and push it to GitHub
8. Create a PR against the `main` branch
