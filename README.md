# den

A CLI utility for local machine automations, built with Python and Typer.

## Installation

### Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) package manager

### Install uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with Homebrew
brew install uv
```

### Install den

```bash
# Clone the repository
git clone <repository-url>
cd den

# Install the package
uv pip install -e .
```

## Usage

### Hello Command

The `hello` command greets a user by name.

```bash
# Default greeting
den hello
# Output: Hello, World!

# Custom name greeting
den hello --name Alice
# Output: Hello, Alice!
```

### Help

```bash
# Show available commands
den --help

# Show hello command options
den hello --help

# Show version
den --version
```

## Development Setup

### Clone and Install

```bash
# Clone the repository
git clone <repository-url>
cd den

# Install with development dependencies
uv pip install -e ".[dev]"
```

### Run Tests

```bash
uv run pytest
```

### Project Structure

```
den/
├── src/
│   └── den/
│       ├── __init__.py
│       ├── main.py
│       └── commands/
│           └── hello.py
├── tests/
├── pyproject.toml
└── README.md
```

## License

MIT
