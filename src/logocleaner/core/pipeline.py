from __future__ import annotations

import numpy as np
from PIL import Image

from logocleaner.core.types import CleaningResult
from logocleaner.masks.alpha import apply_transparency_mask
from logocleaner.strategies.base import BackgroundRemovalStrategy, validate_strategy_mask


def clean_background(
    image: Image.Image,
    strategy: BackgroundRemovalStrategy,
) -> CleaningResult:
    """Clean an image background using the given strategy."""

    rgba_image = image.convert("RGBA")
    image_array = np.asarray(rgba_image, dtype=np.uint8)

    background_mask = strategy.create_mask(image_array)
    validate_strategy_mask(background_mask, image_array)

    result_array = apply_transparency_mask(image_array, background_mask)
    result_image = Image.fromarray(result_array, mode="RGBA")

    return CleaningResult(
        image=result_image,
        background_mask=background_mask,
    )
