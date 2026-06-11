from __future__ import annotations

from pathlib import Path

from PIL import Image

from logocleaner.exceptions import ImageSaveError


def save_png(image: Image.Image, path: Path | str) -> None:
    """Save an RGBA image as PNG."""

    output_path = Path(path)

    if output_path.suffix.lower() != ".png":
        raise ImageSaveError("Output file must be a .png file because transparency is required.")

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(output_path, format="PNG")
    except OSError as exc:
        raise ImageSaveError(f'Could not save image "{output_path}".') from exc
