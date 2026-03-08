.PHONY: clean ruff_fix_imports ruff_format ruff_lint

# --- QA ---

QA_CHECK_DIR := ./src/
QA_EXCLUDE_DIR := ./notebooks/

ruff_fix_imports:
	uv run ruff check --select I --fix $(QA_CHECK_DIR) --exclude $(QA_EXCLUDE_DIR)

ruff_format:
	uv run ruff format $(QA_CHECK_DIR) --exclude $(QA_EXCLUDE_DIR)

ruff_lint:
	uv run ruff check --fix $(QA_CHECK_DIR) --exclude $(QA_EXCLUDE_DIR)

clean:
	find . -type f -name "*.DS_Store" -ls -delete
	find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf
	find . | grep -E ".pytest_cache" | xargs rm -rf
	find . | grep -E ".ipynb_checkpoints" | xargs rm -rf
	rm -rf .coverage*

