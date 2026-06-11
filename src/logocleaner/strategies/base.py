from __future__ import annotations

from typing import Protocol, runtime_checkable

import numpy as np

from logocleaner.core.types import ImageArray, MaskArray
from logocleaner.exceptions import InvalidMaskError


@runtime_checkable
class BackgroundRemovalStrategy(Protocol):
    """Interface for background removal strategies.

    A strategy receives an RGBA image array and returns a boolean mask.

    Mask convention:
        True  -> background pixel, should become transparent.
        False -> foreground/logo pixel, should be preserved.
    """

    @property
    def name(self) -> str:
        """Human-readable strategy name."""
        ...

    def create_mask(self, image: ImageArray) -> MaskArray:
        """Create a background mask for the given RGBA image."""
        ...


def validate_strategy_mask(mask: MaskArray, image: ImageArray) -> None:
    """Validate that a strategy returned a usable background mask."""

    if mask.dtype != np.bool_:
        raise InvalidMaskError("Strategy mask must be a boolean NumPy array.")

    if image.ndim != 3:
        raise InvalidMaskError("Image array must have shape (height, width, channels).")

    if image.shape[2] != 4:
        raise InvalidMaskError("Image array must be RGBA with 4 channels.")

    expected_shape = image.shape[:2]

    if mask.shape != expected_shape:
        raise InvalidMaskError(f"Strategy mask shape must be {expected_shape}, got {mask.shape}.")
