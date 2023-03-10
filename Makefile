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

PLONE6=6.0-latest

BACKEND_FOLDER=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

CODE_QUALITY_VERSION=2.1.0
ifndef LOG_LEVEL
	LOG_LEVEL=INFO
endif
CURRENT_USER=$$(whoami)
USER_INFO=$$(id -u ${CURRENT_USER}):$$(getent group ${CURRENT_USER}|cut -d: -f3)
LINT=docker run --rm -e LOG_LEVEL="${LOG_LEVEL}" -v "${BACKEND_FOLDER}":/github/workspace plone/code-quality:${CODE_QUALITY_VERSION} check
FORMAT=docker run --rm --user="${USER_INFO}" -e LOG_LEVEL="${LOG_LEVEL}" -v "${BACKEND_FOLDER}":/github/workspace plone/code-quality:${CODE_QUALITY_VERSION} format

DOCS_DIR=${BACKEND_FOLDER}/docs


all: build

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

bin/pip:
	@echo "$(GREEN)==> Setup Virtual Env$(RESET)"
	python3 -m venv .
	bin/pip install -U pip wheel

.PHONY: build-plone-6.0
build-plone-6.0: bin/pip ## Build Plone 6.0
	@echo "$(GREEN)==> Build with Plone 6.0$(RESET)"
	bin/pip install Plone -c https://dist.plone.org/release/$(PLONE6)/constraints.txt
	bin/pip install -r requirements.txt
	bin/mkwsgiinstance -d . -u admin:admin

.PHONY: build
build: build-plone-6.0 ## Build Plone 6.0

.PHONY: clean
clean: ## Remove old virtualenv and creates a new one
	@echo "$(RED)==> Cleaning environment and build$(RESET)"
	rm -rf bin lib lib64 include share etc var inituser pyvenv.cfg .installed.cfg

.PHONY: format
format: ## Format the codebase according to our standards
	@echo "$(GREEN)==> Format codebase$(RESET)"
	$(FORMAT)

.PHONY: lint
lint: ## check code style
	$(LINT)

.PHONY: lint-black
lint-black: ## validate black formating
	$(LINT) black

.PHONY: lint-flake8
lint-flake8: ## validate black formating
	$(LINT) flake8

.PHONY: lint-isort
lint-isort: ## validate using isort
	$(LINT) isort

.PHONY: lint-pyroma
lint-pyroma: ## validate using pyroma
	$(LINT) pyroma

.PHONY: lint-zpretty
lint-zpretty: ## validate ZCML/XML using zpretty
	$(LINT) zpretty

# i18n
bin/i18ndude:	bin/pip
	@echo "$(GREEN)==> Install translation tools$(RESET)"
	bin/pip install i18ndude

.PHONY: i18n
i18n: bin/i18ndude ## Update locales
	@echo "$(GREEN)==> Updating locales$(RESET)"
	bin/update_cr_slack_locale

.PHONY: test
test: ## run tests
	bin/pytest --disable-warnings

.PHONY: start
start: ## Start a Plone instance on localhost:8080
	PYTHONWARNINGS=ignore ./bin/runwsgi etc/zope.ini


# Docs
bin/sphinx-build: bin/pip
	bin/pip install -r requirements-docs.txt

.PHONY: build-docs
build-docs: bin/sphinx-build  ## Build the documentation
	./bin/sphinx-build \
		-b html $(DOCS_DIR) "$(DOCS_DIR)/_build/html"

.PHONY: livehtml
livehtml: bin/sphinx-build  ## Rebuild Sphinx documentation on changes, with live-reload in the browser
	./bin/sphinx-autobuild \
		--ignore "*.swp" \
		-b html $(DOCS_DIR) "$(DOCS_DIR)/_build/html"
