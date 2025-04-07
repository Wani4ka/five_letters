.PHONY: lint
lint: install-deps
	flake8 $(shell git ls-files '*.py')

.PHONY: upgrade-pip
upgrade-pip:
	python -m pip install --upgrade pip

.PHONY: install-deps
install-deps: upgrade-pip
	pip install -r requirements.txt
