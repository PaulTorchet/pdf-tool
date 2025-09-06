format:
	pdm run ruff check --select I,F401 --fix
	pdm run ruff format

lint:
	pdm run ruff check