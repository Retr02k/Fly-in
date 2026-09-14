ENV_UV := .venv/bin/uv
REMOVE := rm -fr
MYPY_FLAGS := --warn-return-any --warn-unused-ignores\
			  --ignore-missing-imports --disallow-untyped-defs\
			  --check-untyped-defs

install:
	@echo "Installing dependencies and preparing environment..."
	uv sync

run:
	@echo "Running app..."
	uv run fly-in

test:
	uv run pytest -v

test-fast:
	uv run pytest -x

coverage:
	uv run pytest --cov=src/fly_in --cov-report=term-missing

debug:
	uv run python -m pdb fly-in

lint:
	uv run flake8 .
	uv run mypy . $(MYPY_FLAGS)

lint-strict:
	uv run flake8 .
	uv run mypy . --strict

clean:
	@echo "Cleaning environment..."
	$(REMOVE) .venv
	$(REMOVE) $$(find . -name __pycache__ -o -name .mypy_cache)
