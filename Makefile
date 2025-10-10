.PHONY: format lint test run

format:
	python -m pip install black==24.8.0 isort==5.13.2
	black src tests
	isort src tests

lint:
	python -m pip install flake8==7.1.1
	flake8 src

test:
	pytest -q

run:
	python -m app.cli post --dry-run
