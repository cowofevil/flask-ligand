.DEFAULT_GOAL := help

SHELL := /bin/bash
export VIRTUALENVWRAPPER_PYTHON := /usr/bin/python3

define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

# Launch browser
BROWSER := python3 -c "$$BROWSER_PYSCRIPT"

# pre-commit
PRE_COMMIT_PATH := .git/hooks/pre-commit

.PHONY: help
help:
	@python3 -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

.PHONY: check-venv
check-venv: ## verify that the user is running in a Python virtual environment
	@if [ -z "$(VIRTUALENVWRAPPER_SCRIPT)" ]; then echo 'Python virtualenvwrapper not installed!' && exit 1; fi
	@if [ -z "$(VIRTUAL_ENV)" ]; then echo 'Not running within a virtual environment!' && exit 1; fi

.PHONY: check-pre-commit
check-pre-commit: ## verify that git pre-commit hooks are setup
	@if ! command -v pre-commit &> /dev/null; \
	then echo 'pre-commit not setup! Run "make setup-pre-commit" first!' && exit 1; fi

.PHONY: check-dirty
check-dirty: check-pre-commit ## verify that git is clean and ready to merge
	@git diff --quiet || (echo 'Git staging is dirty!'; exit 1)

.PHONY: setup-pre-commit
setup-pre-commit: check-venv ## setup git pre-commit hooks
	@pre-commit install

.PHONY: clean
clean: clean-build clean-pyc clean-mypy-cache clean-pip-cache clean-test  ## remove all build, test, coverage, artifacts and wipe virtualenv

.PHONY: clean-build
clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -fr {} +

.PHONY: clean-pyc
clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

.PHONY: clean-mypy-cache
clean-mypy-cache: ## clean the mypy cache
	rm -fr .mypy_cache/

.PHONY: clean-pip-cache
clean-pip-cache: ## purge the PIP cache to pull latest packages from PyPI
	@if ! pip3 cache purge 2>/dev/null; then echo 'The PIP cache is empty'; fi

.PHONY: clean-test
clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -f coverage.xml
	rm -fr htmlcov/
	rm -fr .pytest_cache/

.PHONY: clean-venv
clean-venv: check-venv ## remove all packages from current virtual environment
	@source virtualenvwrapper.sh && wipeenv || echo "Skipping wipe of environment"

.PHONY: lint
lint: ## check style with flake8
	@flake8

.PHONY: type-check
type-check: ## check Python types using mypy
	@mypy --install-types --non-interactive flask_ligand app.py setup.py tests

.PHONY: format
format: ## format code using black
	@black flask_ligand app.py setup.py tests

.PHONY: test
test: ## run tests quickly with the default Python
	@pytest tests

.PHONY: test-all
test-all: ## run tests, linting, formatting and type checking on every Python version with tox
	@tox -p

.PHONY: coverage-term
coverage-term: ## check code coverage with a simple terminal report
	@coverage run --source flask_ligand -m pytest
	@coverage report -m

.PHONY: coverage-html
coverage-html: coverage-term ## check code coverage with an HTML report
	@coverage html
	@$(BROWSER) htmlcov/index.html

.PHONY: coverage-xml
coverage-xml: coverage-term ## check code coverage with an XML report
	@coverage xml

.PHONY: install
install: clean ## install the package to the active Python's site-packages
	@python3 setup.py install

.PHONY: install-editable
install-editable: ## install the package in editable mode
	@if pip3 list -e | grep 'flask_ligand'; then echo 'Editable package already installed'; else \
	pip3 install -e .; fi

.PHONY: install-venv
install-venv: clean-venv install ## install the package after wiping the virtual environment

.PHONY: develop
develop: clean ## install necessary packages to setup a dev environment
	@pip3 install -r requirements.txt -r requirements-dev.txt

.PHONY: develop-venv
develop-venv: clean-venv develop ## setup a dev environment after wiping the virtual environment

.PHONY: bump-version
bump-version: check-dirty test-all ## determine the new version number from commits, create release commit, and create a tag.
	@semantic-release version

.PHONY: build
build: check-dirty clean-build ## builds source and wheel package
	@python3 setup.py sdist bdist_wheel
	@ls -l dist

.PHONY: upload
upload: check-dirty ## upload package to PyPI
	@twine upload dist/*

.PHONY: upload-test
upload-test: check-dirty ## upload package to Test PyPI
	@twine upload -r testpypi dist/*

.PHONY: publish
publish: check-dirty ## update changelog, bump version, push changes to git, build and then upload to PyPI
	@semantic-release publish
