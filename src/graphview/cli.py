import typer
from typing_extensions import Annotated
from pathlib import Path

import graphview.core as core

app = typer.Typer(
    help="A tool to help you navigate your markdown notes.", no_args_is_help=True
)

search_app = typer.Typer(
    name="search", help="Search files using a query", no_args_is_help=True
)
app.add_typer(search_app, name="search")

index_app = typer.Typer(
    name="index",
    help="Build or modify the index in this directory",
    no_args_is_help=True,
)
app.add_typer(index_app, name="index")


@search_app.command(
    "file",
    help="Search files based on the file at FILE_PATH with emphasis on the text at LINE_NUMBER",
)
def search_file(
    file_path: Annotated[str, typer.Argument(help="Path to plain text document")],
    line_number: int | None = None,
):
    core.search_file(file_path, line_number)


@search_app.command("text", help="Search files based on the given QUERY")
def search_text(query: str):
    core.search_text(query)


@index_app.command("build", help="Build or rebuild the index in this directory")
def index_build():
    core.build_index(Path.cwd())


def main():
    app()
