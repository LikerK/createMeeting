install:
	poetry install

build: lint
	poetry build

lint:
	poetry run flake8 bot
