import os
import typer
from . import __version__
from .container import *
from .org import tangle as org_tangle, detangle as org_detangle
from rich import print

app = typer.Typer()

@app.command()
def version():
    """Get the current installed version of weborg"""
    print(f"Version: {__version__}")

@app.command()
def config():
    """Get the current configuration of weborg"""
    # print(f"DOCS_PATH: {os.environ.get('DOCS_PATH')}")

@app.command()
def tangle(folder: str = typer.Argument(..., help="The folder where the Org-mode file to tangle are located")):
    """Tangle the org files in the given folder"""
    folder = os.path.abspath(folder)
    org_tangle(folder)

@app.command()
def detangle(folder: str = typer.Argument(..., help="The folder where the source files to detangle are located")):
    """Detangle the source files in the given folder"""
    folder = os.path.abspath(folder)
    org_detangle(folder)

def init():
    """Initialize weborg"""

    # Make sure the Docker image exists on the local system
    if not image_exists():
        print("Building image...")
        image, logs = build_image()
        print(f"Image built [{image.id}]")

    app()

if __name__ == "__main__":
    init()