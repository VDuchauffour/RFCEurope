.PHONY: clean clean-build clean-pyc clean-test clean-misc lint test

# remove all build, test, coverage and Python artifacts
clean: clean-build clean-pyc clean-test clean-misc

# remove build artifacts
clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr wheelhouse/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

# remove Python file artifacts
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

# remove test and coverage artifacts
clean-test:
	rm -f .coverage
	rm -f coverage.xml
	rm -rf htmlcov/
	rm -rf .tox/
	rm -rf .pytest_cache/

# remove other artifacts
clean-misc:
	rm -rf .ruff_cache/
	rm -rf .mypy_cache/

# lint the package
lint:
	black --check .
	ruff check .

# test the package
test: clean-test
	python Tests/test_imports.py -v
	python Tests/test_base_structures.py -v
