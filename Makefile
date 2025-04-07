.PHONY: lint
lint: install-linter
	flake8 $(shell git ls-files '*.py')

.PHONY: upgrade-pip
upgrade-pip:
	python -m pip install --upgrade pip

.PHONY: install-linter
install-linter: upgrade-pip
	pip install flake8 pep8-naming
