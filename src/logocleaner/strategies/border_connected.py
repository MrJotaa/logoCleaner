from __future__ import annotations

from collections import deque
from dataclasses import dataclass

import numpy as np

from logocleaner.core.colors import create_color_distance_map, validate_rgb_color
from logocleaner.core.types import ImageArray, MaskArray, RGBColor
from logocleaner.core.validation import validate_tolerance


@dataclass(frozen=True)
class BorderConnectedStrategy:
    """Remove only background-like pixels connected to the image border.

    This strategy is safer than global color removal for logos that contain
    internal highlights, text, or details similar to the background color.
    """

    background_color: RGBColor
    tolerance: float = 30.0

    def __post_init__(self) -> None:
        object.__setattr__(self, "background_color", validate_rgb_color(self.background_color))
        object.__setattr__(self, "tolerance", validate_tolerance(self.tolerance))

    @property
    def name(self) -> str:
        return "border"

    def create_mask(self, image: ImageArray) -> MaskArray:
        distance_map = create_color_distance_map(image, self.background_color)
        candidate_mask = np.asarray(distance_map <= self.tolerance, dtype=np.bool_)

        return _extract_border_connected_region(candidate_mask)


def _extract_border_connected_region(candidate_mask: MaskArray) -> MaskArray:
    """Return the region of candidate pixels connected to the image border.

    Uses 4-connectivity for the MVP. This is conservative and helps avoid
    leaking through diagonal gaps in logo edges.
    """

    height, width = candidate_mask.shape

    background_mask = np.zeros((height, width), dtype=np.bool_)
    queue: deque[tuple[int, int]] = deque()

    def enqueue_if_candidate(y: int, x: int) -> None:
        if candidate_mask[y, x] and not background_mask[y, x]:
            background_mask[y, x] = True
            queue.append((y, x))

    for x in range(width):
        enqueue_if_candidate(0, x)
        enqueue_if_candidate(height - 1, x)

    for y in range(1, height - 1):
        enqueue_if_candidate(y, 0)
        enqueue_if_candidate(y, width - 1)

    while queue:
        y, x = queue.popleft()

        for next_y, next_x in (
            (y - 1, x),
            (y + 1, x),
            (y, x - 1),
            (y, x + 1),
        ):
            if next_y < 0 or next_y >= height or next_x < 0 or next_x >= width:
                continue

            if candidate_mask[next_y, next_x] and not background_mask[next_y, next_x]:
                background_mask[next_y, next_x] = True
                queue.append((next_y, next_x))

    return background_mask
