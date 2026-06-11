from __future__ import annotations

from enum import Enum
from pathlib import Path
from textwrap import dedent
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

APP_EPILOG = "\n".join(
    [
        "Strategies:",
        "",
        "  global   Remove all pixels similar to the background color. Aggressive.",
        "",
        "  border   Remove only background-like pixels connected to image borders. Safer.",
        "",
        "Examples:",
        "",
        '  logocleaner clean input.png output.png --mode global --bg "#ffffff" --tolerance 40',
        "",
        "  logocleaner clean input.png output.png --mode border --bg auto --tolerance 30",
        "",
        "More info:",
        "",
        "  logocleaner clean --help",
        "",
        "  logocleaner strategies",
    ]
)

CLEAN_EPILOG = "\n".join(
    [
        "Strategies:",
        "",
        "  global   Aggressive. Removes matching pixels anywhere in the image.",
        "",
        "  border   Safer. Removes only matching pixels connected to image borders.",
        "",
        "Examples:",
        "",
        '  logocleaner clean input.png output.png --mode global --bg "#ffffff" --tolerance 40',
        "",
        "  logocleaner clean input.png output.png --mode border --bg auto --tolerance 30",
    ]
)

app = typer.Typer(
    name="logocleaner",
    help="Remove uniform backgrounds from logo images.",
    epilog=APP_EPILOG,
    no_args_is_help=True,
)


@app.callback()
def main() -> None:
    """LogoCleaner command line interface."""


class CleaningMode(str, Enum):
    global_color = "global"
    border = "border"


@app.command(
    help="Remove a uniform background from a logo image.",
    short_help="Remove a logo background.",
    epilog=CLEAN_EPILOG,
)
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


@app.command(
    help="Show available background removal strategies.",
    short_help="Show available strategies.",
)
def strategies() -> None:
    """Show available background removal strategies."""

    typer.echo(
        dedent(
            """\
            Available strategies:

              global
                Removes all pixels similar to the selected background color.
                Best for simple logos on a flat background.
                Risk: can remove internal logo details if they have a similar color.

              border
                Removes only background-like pixels connected to the image border.
                Best for badges, circular, patches, shields, and logos with light internal details.
                Risk: may preserve internal holes that are visually part of the background.

            Examples:

              logocleaner clean input.png output.png --mode global --bg "#ffffff" --tolerance 40
              logocleaner clean input.png output.png --mode border --bg auto --tolerance 30
            """
        )
    )


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
