RUFF      := $(shell which ruff 2>/dev/null || echo uvx ruff)
PRECOMMIT := $(shell which pre-commit 2>/dev/null || echo uvx pre-commit)

all: lint ruff-format

lint:
	$(PRECOMMIT) run -a

ruff-format:
	$(RUFF) format
