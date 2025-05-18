from typer import Typer, Context
from app.cli import hello
from app.cli.config.config import get_config

app = Typer(help="CLI TEMPLATE FOR PYTHON PROJECTS")

app.add_typer(hello.app, name="hello", help="Hello world command")


@app.callback()
def cli(ctx: Context):
    """
    CLI entrypoint – injects config into the Typer context.
    """
    ctx.obj = get_config()


def main():
    app()


if __name__ == "__main__":
    main()
