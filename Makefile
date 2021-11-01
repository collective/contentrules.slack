### Defensive settings for make:
#     https://tech.davis-hansson.com/p/make/
SHELL:=bash
.ONESHELL:
.SHELLFLAGS:=-xeu -o pipefail -O inherit_errexit -c
.SILENT:
.DELETE_ON_ERROR:
MAKEFLAGS+=--warn-undefined-variables
MAKEFLAGS+=--no-builtin-rules

# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

SPHINXOPTS    =
SPHINXAPIDOC  = ./bin/sphinx-apidoc
SPHINXBUILD   = ./bin/sphinx-build
PAPER         =
BUILDDIR      = docs/_build
SOURCEDIR      = docs


PACKAGE_NAME=contenrules.slack
PACKAGE_PATH=/src/contenrules/slack
CHECK_PATH=setup.py $(PACKAGE_PATH)

# User-friendly check for sphinx-build
ifeq ($(shell which $(SPHINXBUILD) >/dev/null 2>&1; echo $$?), 1)
$(error The '$(SPHINXBUILD)' command was not found. Make sure you have Sphinx installed, then set the SPHINXBUILD environment variable to point to the full path of the '$(SPHINXBUILD)' executable. Alternatively you can add the directory with the executable to your PATH. If you dont have Sphinx installed, grab it from http://sphinx-doc.org/)
endif

# Internal variables.
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) $(SOURCEDIR)
# the i18n builder cannot share the environment and doctrees with the others
I18NSPHINXOPTS  = $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .

.PHONY: docs

bin/pip:
	@echo "$(GREEN)==> Setup Virtual Env$(RESET)"
	python3 -m venv .
	bin/pip install -U pip

.PHONY: clean
clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

.PHONY: clean-build
clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

.PHONY: clean-pyc
clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

.PHONY: clean-test
clean-test: ## remove test and coverage artifacts
	rm -f .coverage
	rm -fr htmlcov/

bin/mkwsgiinstance:	bin/pip
	@echo "$(GREEN)==> Install Plone and create instance$(RESET)"
	bin/pip install --use-deprecated=legacy-resolver -r requirements/plone6.txt
	bin/mkwsgiinstance -d . -u admin:admin

.PHONY: build
build: bin/mkwsgiinstance ## Create virtualenv and install package in a Plone 6
	@echo "$(GREEN)==> Setup Build$(RESET)"
	bin/pip install --use-deprecated=legacy-resolver -r requirements.txt

.PHONY: build-dev
build-dev: bin/mkwsgiinstance ## Create virtualenv and install package in a Plone 6
	@echo "$(GREEN)==> Setup Build$(RESET)"
	bin/pip install --use-deprecated=legacy-resolver -r requirements/dev.txt

docs: ## generate Sphinx HTML documentation, including API docs
	rm -rf $(BUILDDIR)/*
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html

.PHONY: black
black: ## Format codebase
	./bin/black $(CHECK_PATH)

.PHONY: isort
isort: ## Format imports in the codebase
	./bin/isort $(CHECK_PATH)

.PHONY: format
format: black isort ## Format the codebase according to our standards

.PHONY: lint
lint: lint-isort lint-black ## check style with flake8

.PHONY: lint-black
lint-black: ## validate black formating
	./bin/black --check --diff $(CHECK_PATH)

.PHONY: lint-isort
lint-isort: ## validate using isort
	./bin/isort --check-only $(CHECK_PATH)

.PHONY: test
test: ## run tests
	./bin/zope-testrunner --auto-color --auto-progress --test-path src/
