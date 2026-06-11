from __future__ import annotations

from dataclasses import dataclass
from numbers import Real

import numpy as np

from logocleaner.core.colors import create_color_distance_map, validate_rgb_color
from logocleaner.core.types import ImageArray, MaskArray, RGBColor
from logocleaner.exceptions import InvalidToleranceError


@dataclass(frozen=True)
class GlobalColorStrategy:
    """Remove all pixels similar to a background color.

    This strategy is aggressive: it removes matching pixels anywhere in the
    image, not only pixels connected to the image border.
    """

    background_color: RGBColor
    tolerance: float = 30.0

    def __post_init__(self) -> None:
        object.__setattr__(self, "background_color", validate_rgb_color(self.background_color))
        object.__setattr__(self, "tolerance", _validate_tolerance(self.tolerance))

    @property
    def name(self) -> str:
        return "global"

    def create_mask(self, image: ImageArray) -> MaskArray:
        distance_map = create_color_distance_map(image, self.background_color)

        return np.asarray(distance_map <= self.tolerance, dtype=np.bool_)


def _validate_tolerance(value: object) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise InvalidToleranceError("Tolerance must be a number.")

    tolerance = float(value)

    if tolerance < 0:
        raise InvalidToleranceError("Tolerance must be >= 0.")

    return tolerance
