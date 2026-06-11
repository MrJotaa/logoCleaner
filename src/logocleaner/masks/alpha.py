from __future__ import annotations

import numpy as np

from logocleaner.core.types import ImageArray, MaskArray
from logocleaner.strategies.base import validate_strategy_mask


def apply_transparency_mask(image: ImageArray, background_mask: MaskArray) -> ImageArray:
    """Apply a background mask to an RGBA image.

    Mask convention:
        True  -> background pixel, alpha becomes 0.
        False -> foreground/logo pixel, alpha is preserved.
    """

    validate_strategy_mask(background_mask, image)

    result = image.copy()
    result[background_mask, 3] = 0

    return np.asarray(result, dtype=np.uint8)
