#########
# Тесты #
#########

# Запускает юнит-тесты
unit-test: install-deps
	pytest -v

##########
# Линтер #
##########

# Запускает линтер
lint: install-deps
	ruff check

# Исправляет некоторые ошибки кодстайла
lint-fix: install-deps
	ruff check . --fix

###############
# Зависимости #
###############

# Устанавливает последнюю версию pip
upgrade-pip:
	python -m pip install --upgrade pip

# Устанавливает зависимости проекта
install-deps: upgrade-pip
	pip install -r requirements.txt

.PHONY: lint upgrade-pip install-deps lint-fix