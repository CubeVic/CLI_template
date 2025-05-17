## 📘 CLI Usage Guide: Typer Basics

This project uses [**Typer**](https://typer.tiangolo.com/) to build command-line interfaces (CLIs). This guide is a quick reference to help you understand how the CLI is structured and how to use and extend it.

---

### 🧠 What is Typer?

Typer is a Python library that makes building CLI tools easy and intuitive by using **type hints**. It automatically generates:

* Help menus
* Parameter parsing
* Argument validation
* Shell autocompletion

It’s built on top of [Click](https://click.palletsprojects.com/) and inspired by [FastAPI](https://fastapi.tiangolo.com/).

---

### 🔧 How Commands Are Structured

The CLI is organized with **Typer command groups**. Each module in `app/cli/` defines a subcommand group.

Example:

```bash
poetry run cli-template hello greet --name Alice
```

* `cli-template`: the top-level CLI (configured in `pyproject.toml`)
* `hello`: a subcommand group
* `greet`: a command within `hello`
* `--name Alice`: an option passed to the command

---

### ✨ Basic Typer Syntax

```python
import typer

app = typer.Typer()

@app.command()
def greet(name: str):
    print(f"Hello, {name}!")
```

Calling:

```bash
python main.py greet --name Alice
```

---

### 📁 Subcommands via `app.add_typer()`

You can split commands into modules and compose them in `main.py`:

```python
# app/cli/hello.py
import typer
app = typer.Typer()

@app.command()
def greet(name: str):
    print(f"Hello, {name}!")
```

Then register in `app/main.py`:

```python
from typer import Typer
from app.cli import hello

app = Typer()
app.add_typer(hello.app, name="hello")
```

Now you can run:

```bash
poetry run cli-template hello greet --name Alice
#poerty run APP_NAME [Groups] <command> `argument` value
```

---

### 🛠 Arguments vs Options

* **Arguments**: Positional and required by default
* **Options**: Named, prefixed by `--`, and optional (with defaults)

```python
@app.command()
def show(
    config_file: str = typer.Argument(..., help="Path to config"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
):
    ...
```

Call:

```bash
cli-template config show ./config.toml --verbose
```

🏗️ Summary of Command Style

```poetry run cli-template <group> <command> [--options]```

Example:

```poetry run cli-template hello greet --name Alice```

| Part           | Meaning                     |
| -------------- | --------------------------- |
| `cli-template` | Your top-level CLI app name |
| `hello`        | Subcommand group            |
| `greet`        | The command under `hello`   |
| `--name Alice` | Named parameter             |

---

### ✅ Best Practices

* Define each subcommand group in a separate file inside `app/cli/`
* Use type hints for all arguments and options
* Add docstrings or `help=` strings to document commands and flags
* Use Rich for pretty output, logging, or styled CLI

---



### 📚 More Resources

* [Typer Docs](https://typer.tiangolo.com/)
* [Typer Examples](https://github.com/tiangolo/typer/tree/master/examples)
* [Click Docs](https://click.palletsprojects.com/)
* [FastAPI Docs](https://fastapi.tiangolo.com/) (similar style)

