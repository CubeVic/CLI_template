from app.cli.config.config import Config
from typer import Context, Typer
from rich import print


app = Typer(help="Hello world command")


@app.command()
def greet(name: str, ctx: Context):
    """
    Hello world command
    """
    config: Config = ctx.obj
    print(f"Hello {name}!")
    print(f"App Name: {config.app.app_name}")
    print(f"all config : {config}")
