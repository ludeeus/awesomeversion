.DEFAULT_GOAL := help

help: ## Shows this help message
	@printf "\033[1m%s\033[36m %s\033[32m %s\033[0m \n\n" "Development environment for" "ludeeus/awesomeversion" "";
	@awk 'BEGIN {FS = ":.*##";} /^[a-zA-Z_-]+:.*?##/ { printf " \033[36m make %-25s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST);
	@echo

requirements: install-poetry ## Install requirements
	@poetry install
	@poetry check

install-poetry:
	@curl -sSL https://install.python-poetry.org | python3 -

test: ## Run all tests
	@python3 -m pytest tests -rxf -x -vv -l -s --cov=./ --cov-report=xml

lint: isort black mypy pylint ## Lint all files


coverage: ## Check the coverage of the package
	@python3 -m pytest tests -rxf -x -v -l --cov=./ --cov-report=xml > /dev/null
	@coverage report

isort:
	@python3 -m isort awesomeversion tests

isort-check:
	@python3 -m isort awesomeversion tests --check-only

black:
	@python3 -m black --fast awesomeversion tests

black-check:
	@python3 -m black --check --fast awesomeversion tests

mypy:
	@python3 -m mypy --strict awesomeversion tests

pylint:
	@python3 -m pylint awesomeversion tests