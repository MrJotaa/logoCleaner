from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Annotated

import numpy as np
import typer

from logocleaner.background.detect import detect_background_color
from logocleaner.core.colors import parse_hex_color
from logocleaner.core.pipeline import clean_background
from logocleaner.exceptions import LogoCleanerError
from logocleaner.image_io.load import load_image
from logocleaner.image_io.save import save_png
from logocleaner.strategies.border_connected import BorderConnectedStrategy
from logocleaner.strategies.global_color import GlobalColorStrategy

app = typer.Typer(
    name="logocleaner",
    help="Remove uniform backgrounds from logo images.",
    no_args_is_help=True,
)


@app.callback()
def main() -> None:
    """LogoCleaner command line interface."""


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
            max=442,
            help="Color distance tolerance.",
        ),
    ] = 30,
) -> None:
    """Remove a uniform background from a logo image."""

    try:
        image = load_image(input_path)
        image_array = np.asarray(image, dtype=np.uint8)

        background_color = _resolve_background_color(bg, image_array)
        strategy = _build_strategy(mode, background_color, tolerance)

        result = clean_background(image, strategy)
        save_png(result.image, output_path)

        removed_pixels = int(result.background_mask.sum())
        total_pixels = int(result.background_mask.size)

        typer.echo(f"Strategy: {strategy.name}")
        typer.echo(f"Background color: {background_color}")
        typer.echo(f"Removed pixels: {removed_pixels}/{total_pixels}")
        typer.echo(f"Saved: {output_path}")

    except LogoCleanerError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1) from exc


def _resolve_background_color(bg: str, image_array: np.ndarray) -> tuple[int, int, int]:
    if bg.lower() == "auto":
        return detect_background_color(image_array)

    return parse_hex_color(bg)


def _build_strategy(
    mode: CleaningMode,
    background_color: tuple[int, int, int],
    tolerance: int,
) -> GlobalColorStrategy | BorderConnectedStrategy:
    if mode == CleaningMode.global_color:
        return GlobalColorStrategy(
            background_color=background_color,
            tolerance=tolerance,
        )

    if mode == CleaningMode.border:
        return BorderConnectedStrategy(
            background_color=background_color,
            tolerance=tolerance,
        )

    raise typer.BadParameter(f"Unsupported mode: {mode}")
