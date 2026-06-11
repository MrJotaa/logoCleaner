from __future__ import annotations

from numbers import Integral

import numpy as np

from logocleaner.core.colors import validate_rgb_color
from logocleaner.core.types import ImageArray, RGBColor
from logocleaner.exceptions import BackgroundColorDetectionError


def detect_background_color(
    image: ImageArray,
    *,
    border_width: int = 1,
    min_alpha: int = 1,
) -> RGBColor:
    """Detect the most likely background color from the image border.

    The MVP assumes logos are usually centered on a mostly uniform background.
    Therefore, the background color is estimated from visible pixels touching
    the image border.

    The returned color is the median RGB value of the sampled border pixels.
    """

    border_width = _validate_int_parameter(
        border_width,
        name="border_width",
        min_value=1,
    )
    min_alpha = _validate_int_parameter(
        min_alpha,
        name="min_alpha",
        min_value=0,
        max_value=255,
    )

    height, width = _validate_rgba_image(image)

    if border_width > min(height, width):
        raise BackgroundColorDetectionError(
            "border_width cannot be larger than the shortest image dimension."
        )

    border_pixels = _extract_border_pixels(image, border_width)

    visible_border_pixels = border_pixels[border_pixels[:, 3] >= min_alpha]

    if visible_border_pixels.size == 0:
        raise BackgroundColorDetectionError(
            "Cannot detect background color because no visible border pixels were found."
        )

    rgb_pixels = visible_border_pixels[:, :3].astype(np.float32)
    median_rgb = np.median(rgb_pixels, axis=0)

    rounded_rgb = np.floor(median_rgb + 0.5).astype(int)

    return validate_rgb_color(
        (
            int(rounded_rgb[0]),
            int(rounded_rgb[1]),
            int(rounded_rgb[2]),
        )
    )


def _extract_border_pixels(image: ImageArray, border_width: int) -> ImageArray:
    """Extract pixels touching the image border without duplicating corners."""

    height, width = image.shape[:2]

    border_mask = np.zeros((height, width), dtype=np.bool_)

    border_mask[:border_width, :] = True
    border_mask[-border_width:, :] = True
    border_mask[:, :border_width] = True
    border_mask[:, -border_width:] = True

    return image[border_mask]


def _validate_rgba_image(image: ImageArray) -> tuple[int, int]:
    if image.ndim != 3 or image.shape[2] != 4:
        raise BackgroundColorDetectionError(
            "Image array must be RGBA with shape (height, width, 4)."
        )

    height, width = image.shape[:2]

    if height == 0 or width == 0:
        raise BackgroundColorDetectionError("Image array cannot be empty.")

    return height, width


def _validate_int_parameter(
    value: object,
    *,
    name: str,
    min_value: int,
    max_value: int | None = None,
) -> int:
    if isinstance(value, bool) or not isinstance(value, Integral):
        raise BackgroundColorDetectionError(f"{name} must be an integer.")

    value = int(value)

    if value < min_value:
        raise BackgroundColorDetectionError(f"{name} must be >= {min_value}.")

    if max_value is not None and value > max_value:
        raise BackgroundColorDetectionError(f"{name} must be <= {max_value}.")

    return value
