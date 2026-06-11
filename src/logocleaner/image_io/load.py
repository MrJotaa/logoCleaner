from __future__ import annotations

from pathlib import Path

from PIL import Image, UnidentifiedImageError

from logocleaner.exceptions import ImageLoadError


def load_image(path: Path | str) -> Image.Image:
    """Load an image from disk and normalize it to RGBA."""

    image_path = Path(path)

    try:
        image = Image.open(image_path)
        return image.convert("RGBA")
    except FileNotFoundError as exc:
        raise ImageLoadError(f'Input image "{image_path}" does not exist.') from exc
    except UnidentifiedImageError as exc:
        raise ImageLoadError(f'Input file "{image_path}" is not a valid image.') from exc
    except OSError as exc:
        raise ImageLoadError(f'Could not load image "{image_path}".') from exc
