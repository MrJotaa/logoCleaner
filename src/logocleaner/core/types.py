from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

import numpy as np
from numpy.typing import NDArray
from PIL import Image

RGBColor: TypeAlias = tuple[int, int, int]
RGBAColor: TypeAlias = tuple[int, int, int, int]

ImageArray: TypeAlias = NDArray[np.uint8]
MaskArray: TypeAlias = NDArray[np.bool_]


@dataclass(frozen=True)
class CleaningResult:
    """Result returned by the core cleaning pipeline."""

    image: Image.Image
    background_mask: MaskArray
