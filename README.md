# Python CLI Template 🚀

A modern, Docker-ready template for building command-line applications in Python using [Typer](https://typer.tiangolo.com/), [Poetry](https://python-poetry.org/), and best practices.

---

## 📦 Features

- ✅ **Typer** for intuitive CLI commands and subcommands
- ⚙️ **Configuration** via `.env` and `config.toml`
- 🧪 **Testing** with `pytest`
- 🧹 **Linting** with `ruff`
- ✅ **Pre-commit hooks** for formatting and code quality
- 🐳 **Docker** support for reproducible builds
- 🛠️ **Makefile** to simplify common tasks
- 🎨 **Rich logging and CLI output**

---

## 🧰 Tech Stack

- Python 3.11+
- Typer (CLI Framework)
- Poetry (Dependency management)
- Docker
- Rich (Logging and output formatting)
- dotenv + toml (Configuration)
- pytest + pre-commit + ruff + isort + black (Developer tooling)

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/your-org/python-cli-template.git
cd python-cli-template

# Install dependencies
poetry install

# Run a sample command
poetry run python app/main.py hello --name Alice
