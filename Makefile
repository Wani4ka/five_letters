#########
# Тесты #
#########

# Запускает юнит-тесты
unit-tests: install-deps
	pytest -v

# Запускает юнит-тесты в выводит покрытие по ним
unit-coverage: install-deps
	coverage run -m pytest -v
	coverage report -m --skip-empty

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

.PHONY: lint upgrade-pip install-deps lint-fix unit-tests unit-coverage