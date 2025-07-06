.DEFAULT_GOAL := help

help: ## Shows this help message
	@printf "\033[1m%s\033[36m %s\033[32m %s\033[0m \n\n" "Development environment for" "ludeeus/awesomeversion" "";
	@awk 'BEGIN {FS = ":.*##";} /^[a-zA-Z_-]+:.*?##/ { printf " \033[36m make %-25s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST);
	@echo

requirements: install-uv ## Install requirements
	@uv sync --dev --all-extras

install: ## Install awesomeversion
	@uv sync --dev --all-extras

install-uv:
	@curl -LsSf https://astral.sh/uv/install.sh | sh

test: ## Run all tests
	@uv run --dev pytest --timeout=10 tests -rxf -x -vv -l -s --cov=./ --cov-report=xml

build: ## Build the package
	@uv build

lint: isort black mypy pylint ## Lint all files

snapshot-update: ## Update test snapshot files
	@uv run --dev pytest tests --snapshot-update  --timeout=10

benchmark:
	@uv run --dev pytest -x --no-cov -vvvvv benchmarks

coverage: ## Check the coverage of the package
	@uv run --dev pytest tests --timeout=10 -rxf -x -v -l --cov=./ --cov-report=xml > /dev/null
	@uv run --dev coverage report

isort:
	@uv run --dev isort awesomeversion tests benchmarks

isort-check:
	@uv run --dev isort awesomeversion tests benchmarks --check-only

black:
	@uv run --dev black --fast awesomeversion tests benchmarks

black-check:
	@uv run --dev black --check --fast awesomeversion tests benchmarks

mypy:
	@uv run --dev mypy --strict awesomeversion tests benchmarks

pylint:
	@uv run --dev pylint awesomeversion tests benchmarks