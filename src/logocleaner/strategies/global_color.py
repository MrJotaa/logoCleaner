from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from logocleaner.core.colors import create_color_distance_map, validate_rgb_color
from logocleaner.core.types import ImageArray, MaskArray, RGBColor
from logocleaner.core.validation import validate_tolerance


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
        object.__setattr__(self, "tolerance", validate_tolerance(self.tolerance))

    @property
    def name(self) -> str:
        return "global"

    def create_mask(self, image: ImageArray) -> MaskArray:
        distance_map = create_color_distance_map(image, self.background_color)

        return np.asarray(distance_map <= self.tolerance, dtype=np.bool_)
