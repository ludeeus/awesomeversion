# Copilot instructions for AwesomeVersion

This is a Python package for version parsing and comparison that supports multiple version schemes including semver, calver, 0ver, pep440, and buildver. It provides a unified interface to handle any version format through strategy-based parsing.

## Project overview

AwesomeVersion is a zero-dependency Python library that can parse and compare versions across different versioning schemes. The library is designed to be fast, reliable, and comprehensive in handling various version formats.

## Code standards

### Required before each commit

- Run `./script/lint` to format code with isort and black
- Run `./script/test` to ensure all tests pass
- Use the provided scripts in the `script/` directory for consistency

### Development workflow

- **Setup**: `./script/setup` - Install dependencies and set up development environment
- **Test**: `./script/test` - Run the full test suite with pytest
- **Lint**: `./script/lint` - Format and lint code (isort + black)
- **Lint check**: `./script/lint-check` - Check code formatting without making changes
- **Coverage**: `./script/coverage` - Generate test coverage reports
- **Build**: `./script/build` - Build the package

## Repository structure

- `awesomeversion/` - Main package source code
  - `awesomeversion.py` - Core AwesomeVersion class implementation
  - `strategy.py` - Version strategy definitions and matching logic
  - `exceptions.py` - Custom exception classes
  - `typing.py` - Type definitions
  - `comparehandlers/` - Version comparison logic for different strategies
  - `utils/` - Utility functions for validation and regex operations
- `tests/` - Test suite using pytest
  - `test_*.py` - Main test files
  - `issues/` - Tests for specific GitHub issues
  - `snapshots/` - Snapshot testing data
  - `utils/` - Test utilities
- `benchmarks/` - Performance benchmarking tests
- `script/` - Development scripts following "Scripts to Rule Them All" pattern
- `demo/` - Demo files and examples

## Key development guidelines

### 1. Code style and formatting

- **Python version**: Support Python 3.9+ (as specified in pyproject.toml)
- **Zero dependencies**: This library has no runtime dependencies - keep it that way
- **Type hints**: Use comprehensive type hints throughout (py.typed marker is present)
- **Docstrings**: Follow Google-style docstrings for classes and public methods, using Microsoft Style Guide conventions for clarity and consistency
- **Import style**: Use `from __future__ import annotations` for forward compatibility
- **DRY principle**: Keep all code DRY (Don't Repeat Yourself) - extract common functionality into reusable functions or methods (not required for tests)
- **Efficiency**: All code must be efficient - use caching, memoization, and optimized algorithms where appropriate

### 2. Version strategy implementation

- When adding new version strategies, update `strategy.py` with proper regex patterns
- Each strategy should have corresponding comparison handlers in `comparehandlers/`
- Ensure new strategies are properly tested with edge cases
- Update `COMPARABLE_STRATEGIES` when adding strategies that support comparison

### 3. Testing standards

- **Comprehensive coverage**: Maintain high test coverage (use `./script/coverage`)
- **Snapshot testing**: Use snapshots for regression testing of version parsing
- **Edge cases**: Test boundary conditions, malformed inputs, and error scenarios
- **Performance**: Include benchmarks for performance-critical changes
- **Issue tests**: Add specific tests in `tests/issues/` for GitHub issue fixes

### 4. Error handling

- Use custom exceptions from `exceptions.py` for specific error conditions
- Provide clear, helpful error messages that guide users to correct usage
- Validate inputs early and fail fast with meaningful messages

### 5. Backwards compatibility
- This library is used by many projects - maintain API compatibility
- Deprecate features gracefully before removal
- Follow semantic versioning for releases

## Performance considerations

- Version parsing should be fast - this library is often used in hot paths
- Use compiled regex patterns (already implemented in `utils/regex.py`)
- Cache expensive operations where appropriate using `@cached_property`, `@lru_cache`, or custom caching
- Consider memory usage for large-scale version comparison operations
- Optimize for common use cases while maintaining flexibility for edge cases
- Avoid redundant calculations - cache results of expensive operations
- Use efficient data structures and algorithms

## Specific implementation patterns

### Adding new version strategies

1. Define regex pattern in `strategy.py`
2. Add strategy to appropriate strategy collections
3. Implement comparison logic in `comparehandlers/`
4. Add comprehensive tests including edge cases
5. Update documentation if the strategy is user-facing

### Exception handling

```python
from .exceptions import AwesomeVersionException, AwesomeVersionStrategyException

# Raise specific exceptions for different error types
if not valid_version:
    raise AwesomeVersionException("Version format is invalid")
    
if strategy_mismatch:
    raise AwesomeVersionStrategyException("Version doesn't match required strategy")
```

### Type safety

- Use `VersionType` and other types from `typing.py`
- Leverage `TYPE_CHECKING` for import optimization
- Maintain compatibility with mypy and other type checkers

### Code efficiency patterns

- Use `@cached_property` for expensive computed properties that don't change
- Use `@lru_cache` from `functools` for expensive function calls with repeated inputs
- Implement custom caching for complex scenarios where built-in caching isn't sufficient
- Extract common logic into utility functions to avoid duplication
- Prefer early returns and guard clauses to reduce nesting

## Testing guidelines

### Running tests

- Use `./script/test` for full test suite
- Use `./script/test path/to/specific_test.py` for targeted testing
- Snapshots are automatically updated when needed

### Writing tests

- Follow the existing pattern in `test_awesomeversion.py`
- Use descriptive test names that explain what is being tested
- Group related tests in the same file
- Use pytest fixtures for common test data

### Benchmark tests
- Add benchmarks for performance-critical features
- Use the existing benchmark structure in `benchmarks/`
- Ensure benchmarks are deterministic and meaningful

## Documentation standards

- Keep README.md updated with new features and usage examples
- Use clear, concise examples that users can copy-paste
- Document any breaking changes in release notes
- Include type information in documentation examples
- Follow Microsoft Style Guide (MSG) conventions:
  - Use sentence-style capitalization for headings and UI elements
  - Write in active voice and present tense when possible
  - Use parallel structure in lists and procedures
  - Be concise and scannable
  - Use "you" to address the reader directly
- For Markdown content specifically, also follow Google's documentation style guide (https://google.github.io/styleguide/docguide/style.html):
  - Use ATX-style headings (`#` instead of underlines)
  - **ALWAYS put a blank line before and after headings** - this is mandatory
  - Use backticks for code elements, filenames, and technical terms
  - Use numbered lists for procedures, bullet lists for non-sequential items
  - Keep line length reasonable (aim for 80-100 characters)
  - Use consistent indentation (2 spaces for nested lists)
  - Put links at the end of sentences when possible

## Git workflow

- Use conventional commit messages
- Keep commits focused and atomic
- Include tests with feature additions
- Update documentation for user-facing changes


## Notes for Copilot

- This codebase emphasizes performance, reliability, and backwards compatibility
- Version parsing logic is complex - ensure thorough testing of any changes
- The library supports many edge cases in version formats - maintain this flexibility
- Use the existing script system rather than running commands directly
- Pay attention to type safety and maintain the zero-dependency principle
- When in doubt, follow the patterns established in existing code rather than introducing new patterns
- **Do not add inline comments to code unless specifically requested by the user.**

## Updating these instructions

When the project author provides new requirements, guidelines, or constraints that are not covered by these existing instructions:

1. **Add the new requirements** to the appropriate section of this file
2. **Update existing sections** if the new requirements conflict with or enhance current guidelines
3. **Maintain consistency** with the established style and format of these instructions
4. **Follow the same documentation standards** outlined above when updating this file
5. **Test that changes work** by ensuring any code following the updated instructions meets all completion requirements

## Completion requirements

Before considering any code generation or changes complete, ensure all of the following pass:

1. **Tests must pass**: Run `./script/test` - all tests must pass without errors
2. **Linting must be clean**: Run `./script/lint` - code must be properly formatted and linted
3. **Coverage must be 100%**: Run `./script/coverage` - test coverage must remain at 100%

Any pull request or code changes that don't meet these requirements should be considered incomplete. If coverage drops below 100%, add the necessary tests to restore full coverage.
