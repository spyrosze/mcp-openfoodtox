# ensures the target always runs, even if a file with that name exists
.PHONY: setup venv sync db welcome dev run claude test

# Main setup target - runs all setup steps in sequence
setup: venv sync db welcome

# Create virtual environment (idempotent - safe to run multiple times)
venv:
	uv venv

# Install dependencies
sync:
	uv sync

# Set up the database
db:
	uv run python scripts/setup_db.py

welcome:
	uv run python scripts/prompt_welcome.py


# independent target for installing to Claude Desktop
claude:
	uv run python scripts/install_to_claude_desktop.py

# independent target for testing with MCP Inspector
dev:
	uv run mcp dev main.py

# independent target for running the server locally
run:
	uv run python main.py

# Run tests (all tests by default, or specify TEST_PATH=path/to/test_file.py)
test:
	uv run pytest $(if $(TEST_PATH),$(TEST_PATH),tests/)