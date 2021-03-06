.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

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

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-heat
	rm -fr analysis/EGO
	rm -fr analysis/NL2SOL
	rm -fr analysis/MULTIDIM_PARAM
	find . -name '*.out' -exec rm -fr {} +
	find . -name '*.log' -exec rm -fr {} +
	find . -name '*.rst' -exec rm -fr {} +
	find . -name 'analysis/*.dat' -exec rm -fr {} +
	find . -name '*.13' -exec rm -fr {} +
	find . -name '*.png' -exec rm -fr {} +

clean-heat: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr heat/build/
	rm -fr heat/dist/
	rm -fr heat/.eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr heat/.tox/
	rm -f heat/.coverage
	rm -fr heat/htmlcov/
	rm -fr heat/.pytest_cache

install-heat:
	python setup.py develop --user

install: clean install-heat
	chmod +x analysis/start_01_grid.sh
	chmod +x analysis/start_02_nl2sol.sh
	chmod +x analysis/start_03_ego.sh
	python figures/make_black_box_plot.py

install-hydroshare: clean install-heat
	python figures/make_black_box_plot.py
