import datetime
import os.path
import platform
import shutil
from pathlib import Path

import typer
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from typing_extensions import Annotated


# Tagging tools
curr_time = datetime.datetime.now().strftime("%m-%d-%y")

# Typer application CLI
console = Console()
app = typer.Typer(
    context_settings={"help_option_names": ["-h", "--help"]},
    rich_markup_mode="markdown",
    epilog="Author: William Li :sunglasses:",
)


def os_check():
    """Verify the operation system is Mac.  Mac was forked from UNIX and called Darwin.

    Raises:
        ValueError: Raises error if the OS is not Mac.
    """
    if "darwin" not in platform.system().lower():
        raise ValueError("This script was designed to run on Mac OS")


os_check()


@app.command(
    help=":mountain: **Create** a new VSCode image.",
)
def create_image(
    image_dest: Annotated[
        str, typer.Option(help="path to the image")
    ] = f"images/vscode_image_{curr_time}",
):
    """Create an image of VsCode by creating a directory and copying all of the files and folders needed to snapshot the current installation.  This includes copying:

    * VsCode
    * User Profiles
    * Extensions
    * Misc VsCode files

    Args:
        image_dest (Annotated[ str, typer.Option, optional): The image will be saved to the current working directory at under `images` and tagged with the current date by default. Defaults to "path to the image") ]=f"images/vscode_image_{curr_time}".
    """
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
)
def restore_image(
    image_dest: Annotated[str, typer.Option(help="path to the image")] = "None",
):
    """Restore VsCode from a previously saved image.  You must provide the path to the image you want to source from.

    Args:
        image_dest (Annotated[str, typer.Option, optional): The source path of the image to restore from. Defaults to "path to the image")]="None".

    Raises:
        ValueError: Warning to user that a path must be provided.
    """
    if image_dest == "None":
        raise ValueError("Must provide an image to restore from!")

    # Get the VSCode paths and restore from image
    vscode_paths = get_vscode_paths()
    home = os.path.expanduser("~")

    for src_path, img_path in vscode_paths:
        src_dir = f"{image_dest}/{img_path}"
        img_dir = f"{home}/{src_path}"
        shutil.copytree(src_dir, img_dir, dirs_exist_ok=True)


@app.command(
    help=":mountain: **Uninstall** the current VSCode. Must run with sudo privileges by invoking the CLI with sudo...",
)
def uninstall():
    """Completely uninstall the VsCode on your current MacOS system.  This will delete everything including extensions and user settings!  This cannot be undone!"""

    home = os.path.expanduser("~")

    dirs_to_remove = [
        f"/Applications/Visual Studio Code.app",
        f"{home}/Library/Preferences/com.microsoft.VSCode.plist",
        f"{home}/Library/Application Support/Code/",
        f"{home}/Library/Caches/com.microsoft.VSCode",
        f"{home}/Library/Caches/com.microsoft.VSCode.ShipIt/",
        f"{home}/Library/Saved Application State/com.microsoft.VSCode.savedState/",
        f"{home}/.vscode/",
    ]

    for dir in dirs_to_remove:
        if os.path.isfile(dir):
            os.remove(dir)
            print(f":boom: Successfully removed: {dir}")
        elif os.path.isdir(dir):
            shutil.rmtree(dir)
            print(f":boom: Successfully removed: {dir}")
        else:
            print(f":x: Could not remove: {dir}")


def get_vscode_paths() -> list[tuple[str, str]]:
    """A list of all paths that must be copied from in order to create a VsCode image.

    Returns:
        list[tuple[str, str]]: A list of tuples with path and files/folders for VsCode
    """
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
