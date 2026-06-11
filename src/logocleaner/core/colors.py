from __future__ import annotations

import math
import re
from numbers import Integral

import numpy as np
from numpy.typing import NDArray

from logocleaner.core.types import ImageArray, RGBColor
from logocleaner.exceptions import InvalidColorError

_HEX_COLOR_PATTERN = re.compile(r"^#[0-9a-fA-F]{6}$")


def parse_hex_color(value: str) -> RGBColor:
    """Parse a hex color in #RRGGBB format."""

    if not isinstance(value, str):
        raise InvalidColorError("Color must be a string in #RRGGBB format.")

    if not _HEX_COLOR_PATTERN.match(value):
        raise InvalidColorError(f'Invalid color "{value}". Expected format: #RRGGBB.')

    return (
        int(value[1:3], 16),
        int(value[3:5], 16),
        int(value[5:7], 16),
    )


def validate_rgb_color(color: object) -> RGBColor:
    """Validate and return an RGB color.

    Accepts tuple/list-like values with exactly three integer channels.
    Returns a normalized tuple[int, int, int].
    """

    if isinstance(color, str | bytes):
        raise InvalidColorError("RGB color must be a sequence of 3 integer channels.")

    try:
        channels = tuple(color)  # type: ignore[arg-type]
    except TypeError as exc:
        raise InvalidColorError("RGB color must be a sequence of 3 integer channels.") from exc

    if len(channels) != 3:
        raise InvalidColorError("RGB color must have exactly 3 channels.")

    validated_channels: list[int] = []

    for channel in channels:
        if isinstance(channel, bool) or not isinstance(channel, Integral):
            raise InvalidColorError("RGB color channels must be integers.")

        channel_value = int(channel)

        if channel_value < 0 or channel_value > 255:
            raise InvalidColorError("RGB color channels must be between 0 and 255.")

        validated_channels.append(channel_value)

    return (
        validated_channels[0],
        validated_channels[1],
        validated_channels[2],
    )


def color_distance(color_a: RGBColor, color_b: RGBColor) -> float:
    """Calculate Euclidean distance between two RGB colors."""

    validate_rgb_color(color_a)
    validate_rgb_color(color_b)

    return math.sqrt(
        (color_a[0] - color_b[0]) ** 2
        + (color_a[1] - color_b[1]) ** 2
        + (color_a[2] - color_b[2]) ** 2
    )


def create_color_distance_map(image: ImageArray, background_color: RGBColor) -> NDArray[np.float32]:
    """Create a per-pixel RGB distance map against a background color.

    The returned array has shape (height, width), where each value is the
    Euclidean RGB distance between that pixel and the background color.
    """

    validate_rgb_color(background_color)

    if image.ndim != 3 or image.shape[2] != 4:
        raise InvalidColorError("Image array must be RGBA with shape (height, width, 4).")

    rgb = image[:, :, :3].astype(np.int32)
    target = np.array(background_color, dtype=np.int32)

    diff = rgb - target
    distances = np.sqrt(np.sum(diff * diff, axis=2))

    return distances.astype(np.float32)
