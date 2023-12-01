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
from pathlib import Path


# Tagging tools
curr_time = datetime.datetime.now().strftime("%m-%d-%y")

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
    ] = f"images/vscode_image_{curr_time}",
):
    # Create the directory if it does not exist
    Path(image_dest).mkdir(parents=True, exist_ok=True)

    # Get the VSCode paths and create image
    vscode_paths = get_vscode_paths()
    home = os.path.expanduser("~")

    for src_path, img_path in vscode_paths:
        src_dir = f"{home}/{src_path}"
        img_dir = f"{image_dest}/{img_path}"
        shutil.copytree(src_dir, img_dir, dirs_exist_ok=True)


@app.command(
    help=":mountain: **Restores** a VSCode image.",
    epilog="Author: William Li :sunglasses:",
)
def restore_image(
    image_dest: Annotated[str, typer.Option(help="path to the image")] = "None",
):
    if image_dest == "None":
        raise ValueError("Must provide an image to restore from!")

    # Get the VSCode paths and restore from image
    vscode_paths = get_vscode_paths()
    home = os.path.expanduser("~")

    for src_path, img_path in vscode_paths:
        src_dir = f"{image_dest}/{img_path}"
        img_dir = f"{home}/{src_path}"
        shutil.copytree(src_dir, img_dir, dirs_exist_ok=True)


def get_vscode_paths():
    paths = [
        (
            "Library/Caches/com.microsoft.VSCode",
            "com.microsoft.VSCode",
        ),
        (
            "Library/Caches/com.microsoft.VSCode.ShipIt",
            "com.microsoft.VSCode.ShipIt",
        ),
        (
            "Library/Application Support/Code",
            "Code",
        ),
        (
            "Library/Saved Application State/com.microsoft.VSCode.savedState",
            "com.microsoft.VSCode.savedState",
        ),
        (
            ".vscode",
            ".vscode",
        ),
    ]

    return paths


if __name__ == "__main__":
    app()
