# Запускает линтер
lint: install-deps
	ruff check

# Исправляет некоторые ошибки кодстайла
lint-fix: install-deps
	ruff check . --fix

# Устанавливает последнюю версию pip
upgrade-pip:
	python -m pip install --upgrade pip

# Устанавливает зависимости проекта
install-deps: upgrade-pip
	pip install -r requirements.txt

.PHONY: lint upgrade-pip install-deps lint-fix