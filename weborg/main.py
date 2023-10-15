import os
import time
import typer
from . import __version__
from .container import *
from .monitor import OrgFileChangeHandler
from .org import tangle as org_tangle, detangle as org_detangle
from rich import print
from typing import List
from typing_extensions import Annotated
from watchdog.observers import Observer

app = typer.Typer()

@app.command()
def version():
    """Get the current installed version of weborg"""
    print(f"Version: {__version__}")

@app.command()
def config():
    """Get the current configuration of weborg"""
    # print(f"DOCS_PATH: {os.environ.get('DOCS_PATH')}")


# Example: weborg tangle 'org/' --files=test.org --files=foo.org
@app.command()
def tangle(folder: str = typer.Argument(..., help="The folder where the Org-mode files to tangle are located"),
           file: Annotated[List[str], 
                           typer.Option("--file",
                           help="Optional list of one or more files to tangle from `folder`")] = None):
    """Tangle the org files in the given folder"""
    folder = os.path.abspath(folder)
    org_tangle(folder, file)

@app.command()
def detangle(folder: str = typer.Argument(..., help="The folder where the source files to detangle are located"),
             file: Annotated[List[str], 
                           typer.Option("--file",
                           help="Optional list of one or more files to tangle from `folder`")] = None):
                           
    """Detangle the source files in the given folder"""
    folder = os.path.abspath(folder)
    org_detangle(folder, file)

@app.command()
def monitor(folder: str = typer.Argument(..., help="The folder to monitor for changes")):
    """Monitor the given folder for changes and tangle the org files when they change"""
    folder = os.path.abspath(folder)
    event_handler = OrgFileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=folder, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()

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