#########
# Тесты #
#########

# Запускает юнит-тесты
unit-tests: install-deps
	pytest -v test/unit

# Запускает юнит-тесты в выводит покрытие по ним
unit-coverage: install-deps
	coverage run -m pytest -v test/unit
	coverage report -m --skip-empty

# Запускает e2e-тесты, полагая запущенный сервер на порту 8008
e2e-tests: install-deps
	pytest -v test/server

# Запускает e2e-тесты, предварительно выполняя "coverage run server.py" фоном
e2e-tests-bundled: install-deps
	RUN_BUNDLED_SERVER=true pytest -v test/server

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