import logging
from typing import Annotated
import typer

from gt.core import exec_and_store

_logger = logging.getLogger(__name__)

app = typer.Typer()


@app.command()
def run(source_folder: Annotated[str, typer.Argument(help='test suites folder')],
        target_folder: Annotated[str, typer.Argument(help='destination folder with results')]):
    """
    Iterate over all test suites and execute all tests and store results into target folder.
    """
    exec_and_store(source_folder,
                   target_folder,
                   generate_dot=False)


if __name__ == "__main__":
    app()
