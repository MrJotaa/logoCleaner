import numpy as np
import pytest

from logocleaner.exceptions import InvalidMaskError
from logocleaner.strategies.base import validate_strategy_mask


def test_validate_strategy_mask_accepts_boolean_mask_matching_image_shape():
    image = np.zeros((10, 20, 4), dtype=np.uint8)
    mask = np.zeros((10, 20), dtype=np.bool_)

    validate_strategy_mask(mask, image)


def test_validate_strategy_mask_rejects_non_boolean_mask():
    image = np.zeros((10, 20, 4), dtype=np.uint8)
    mask = np.zeros((10, 20), dtype=np.uint8)

    with pytest.raises(InvalidMaskError):
        validate_strategy_mask(mask, image)


def test_validate_strategy_mask_rejects_wrong_shape():
    image = np.zeros((10, 20, 4), dtype=np.uint8)
    mask = np.zeros((20, 10), dtype=np.bool_)

    with pytest.raises(InvalidMaskError):
        validate_strategy_mask(mask, image)


def test_validate_strategy_mask_rejects_non_rgba_image():
    image = np.zeros((10, 20, 3), dtype=np.uint8)
    mask = np.zeros((10, 20), dtype=np.bool_)

    with pytest.raises(InvalidMaskError):
        validate_strategy_mask(mask, image)
