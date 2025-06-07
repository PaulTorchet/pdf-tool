format:
	pdm run ruff check --select I,F401
	pdm run ruff format

lint:
	pdm run ruff check