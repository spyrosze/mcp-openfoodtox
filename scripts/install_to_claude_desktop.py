#!/usr/bin/env python3
"""
Automatically install MCP server to Claude Desktop.
Detects paths and generates the correct configuration.
"""
import json
import os
import platform
from pathlib import Path


def find_claude_config():
    """Find Claude Desktop config file location."""
    system = platform.system()
    home = Path.home()

    if system == "Darwin":  # macOS
        config_path = home / "Library/Application Support/Claude/claude_desktop_config.json"
    elif system == "Windows":
        config_path = home / "AppData/Roaming/Claude/claude_desktop_config.json"
    else:  # Linux
        config_path = home / ".config/Claude/claude_desktop_config.json"

    return config_path


def get_project_root():
    """Get absolute path to project root."""
    return Path(__file__).parent.parent.absolute()


def get_venv_python():
    """Get path to venv Python."""
    project_root = get_project_root()
    venv_python = project_root / ".venv" / "bin" / "python"

    if not venv_python.exists():
        raise FileNotFoundError(
            f"Virtual environment not found at {venv_python}. " "Run 'uv venv' and 'uv sync' first."
        )

    return str(venv_python)


def install_to_claude():
    """Install MCP server to Claude Desktop config."""
    config_path = find_claude_config()
    project_root = get_project_root()
    venv_python = get_venv_python()
    main_py = str(project_root / "main.py")

    # Read existing config or create new
    if config_path.exists():
        with open(config_path, "r") as f:
            config = json.load(f)
    else:
        config = {"mcpServers": {}, "preferences": {}}

    # Ensure mcpServers exists
    if "mcpServers" not in config:
        config["mcpServers"] = {}

    # Add/update our server
    config["mcpServers"]["mcp-openfoodtox"] = {"command": venv_python, "args": [main_py]}

    # Create config directory if needed
    config_path.parent.mkdir(parents=True, exist_ok=True)

    # Write config
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"✅ Successfully installed to Claude Desktop!")
    print(f"   Config file: {config_path}")
    print(f"   Command: {venv_python}")
    print(f"   Args: {main_py}")
    print(f"\n⚠️  Restart Claude Desktop for changes to take effect.")


if __name__ == "__main__":
    try:
        install_to_claude()
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)
