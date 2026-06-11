from enum import Enum
from pathlib import Path
from typing import Annotated

import typer

app = typer.Typer(
    name="logocleaner",
    help="Remove uniform backgrounds from logo images.",
    no_args_is_help=True,
)


class CleaningMode(str, Enum):
    global_color = "global"
    border = "border"


@app.command()
def clean(
    input_path: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            help="Input image path.",
        ),
    ],
    output_path: Annotated[
        Path,
        typer.Argument(
            help="Output PNG path.",
        ),
    ],
    mode: Annotated[
        CleaningMode,
        typer.Option(
            "--mode",
            "-m",
            help="Cleaning strategy to use: global or border.",
        ),
    ],
    bg: Annotated[
        str,
        typer.Option(
            "--bg",
            help='Background color. Use "auto" or a hex color like "#ffffff".',
        ),
    ] = "auto",
    tolerance: Annotated[
        int,
        typer.Option(
            "--tolerance",
            "-t",
            min=0,
            max=441,
            help="Color distance tolerance.",
        ),
    ] = 30,
) -> None:
    if output_path.suffix.lower() != ".png":
        raise typer.BadParameter("Output file must be a .png file.")

    typer.echo(f"Input: {input_path}")
    typer.echo(f"Output: {output_path}")
    typer.echo(f"Mode: {mode.value}")
    typer.echo(f"Background: {bg}")
    typer.echo(f"Tolerance: {tolerance}")