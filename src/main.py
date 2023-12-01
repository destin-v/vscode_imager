import datetime
import os.path


import typer
from rich import print
from rich.console import Console
from rich.panel import Panel
from typing_extensions import Annotated
from rich.table import Table
import shutil
import platform

# Tagging tools
curr_time = datetime.datetime.now().strftime("%m-%d-%y")
userid = os.getenv("USER")

# Typer application CLI
console = Console()
app = typer.Typer(
    context_settings={"help_option_names": ["-h", "--help"]},
    rich_markup_mode="markdown",
)


def os_check():
    if "darwin" not in platform.system().lower():
        raise ValueError("This script was designed to run on Mac OS")


os_check()


@app.command(
    help=":mountain: **Create** a new VSCode image.",
    epilog="Author: William Li :sunglasses:",
)
def create_image(
    image_dest: Annotated[
        str, typer.Option(help="path to the image")
    ] = f"vscode_image_{curr_time}/",
):
    home = os.path.expanduser("~")

    shutil.copytree(
        f"{home}/Library/Caches/com.microsoft.VSCode",
        image_dest,
        dirs_exist_ok=True,
    )
    shutil.copytree(
        f"{home}/Library/Caches/com.microsoft.VSCode.ShipIt",
        image_dest,
        dirs_exist_ok=True,
    )
    shutil.copytree(
        f"{home}/Library/Application Support/Code",
        image_dest,
        dirs_exist_ok=True,
    )
    shutil.copytree(
        f"{home}/Library/Saved Application State/com.microsoft.VSCode.savedState",
        image_dest,
        dirs_exist_ok=True,
    )
    shutil.copytree(
        f"{home}/.vscode",
        image_dest,
        dirs_exist_ok=True,
    )


@app.command(
    help=":mountain: **Restores** a VSCode image.",
    epilog="Author: William Li :sunglasses:",
)
def restore_image(
    image_dest: Annotated[str, typer.Option(help="path to the image")] = "None",
):
    if image_dest == "None":
        raise ValueError("Must provide an image to restore from!")

    home = os.path.expanduser("~")

    shutil.copytree(
        f"{image_dest}/com.microsoft.VSCode",
        f"{home}/Library/Caches/com.microsoft.VSCode",
        dirs_exist_ok=True,
    )
    shutil.copytree(
        f"{image_dest}/com.microsoft.VSCode.ShipIt",
        f"{home}/Library/Caches/com.microsoft.VSCode.ShipIt",
        dirs_exist_ok=True,
    )
    shutil.copytree(
        f"{image_dest}/Code",
        f"{home}/Library/Application Support/Code",
        dirs_exist_ok=True,
    )
    shutil.copytree(
        f"{image_dest}/com.microsoft.VSCode.savedState",
        f"{home}/Library/Saved Application State/com.microsoft.VSCode.savedState",
        dirs_exist_ok=True,
    )
    shutil.copytree(
        f"{image_dest}/.vscode",
        f"{home}/.vscode",
        dirs_exist_ok=True,
    )


if __name__ == "__main__":
    app()
