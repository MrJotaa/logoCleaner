import numpy as np
import pytest

from logocleaner.exceptions import InvalidColorError, InvalidToleranceError
from logocleaner.strategies.base import BackgroundRemovalStrategy, validate_strategy_mask
from logocleaner.strategies.global_color import GlobalColorStrategy


def test_global_color_strategy_matches_strategy_interface():
    strategy = GlobalColorStrategy(background_color=(255, 255, 255), tolerance=30)

    assert isinstance(strategy, BackgroundRemovalStrategy)


def test_global_color_strategy_has_name():
    strategy = GlobalColorStrategy(background_color=(255, 255, 255), tolerance=30)

    assert strategy.name == "global"


def test_global_color_strategy_removes_exact_background_pixels():
    image = np.full((3, 3, 4), [255, 255, 255, 255], dtype=np.uint8)
    image[1, 1] = [255, 0, 0, 255]

    strategy = GlobalColorStrategy(background_color=(255, 255, 255), tolerance=0)

    mask = strategy.create_mask(image)

    expected_mask = np.array(
        [
            [True, True, True],
            [True, False, True],
            [True, True, True],
        ],
        dtype=np.bool_,
    )

    np.testing.assert_array_equal(mask, expected_mask)
    validate_strategy_mask(mask, image)


def test_global_color_strategy_uses_tolerance():
    image = np.array(
        [
            [[255, 255, 255, 255], [250, 250, 250, 255]],
            [[240, 240, 240, 255], [0, 0, 0, 255]],
        ],
        dtype=np.uint8,
    )

    strategy = GlobalColorStrategy(background_color=(255, 255, 255), tolerance=10)

    mask = strategy.create_mask(image)

    expected_mask = np.array(
        [
            [True, True],
            [False, False],
        ],
        dtype=np.bool_,
    )

    np.testing.assert_array_equal(mask, expected_mask)


def test_global_color_strategy_returns_boolean_mask_matching_image_shape():
    image = np.full((10, 20, 4), [255, 255, 255, 255], dtype=np.uint8)

    strategy = GlobalColorStrategy(background_color=(255, 255, 255), tolerance=30)

    mask = strategy.create_mask(image)

    assert mask.dtype == np.bool_
    assert mask.shape == (10, 20)


def test_global_color_strategy_does_not_mutate_input_image():
    image = np.full((3, 3, 4), [255, 255, 255, 255], dtype=np.uint8)
    original = image.copy()

    strategy = GlobalColorStrategy(background_color=(255, 255, 255), tolerance=30)
    strategy.create_mask(image)

    np.testing.assert_array_equal(image, original)


@pytest.mark.parametrize(
    "background_color",
    [
        (-1, 255, 255),
        (255, 256, 255),
        (255, 255),
        "ffffff",
    ],
)
def test_global_color_strategy_rejects_invalid_background_color(background_color):
    with pytest.raises(InvalidColorError):
        GlobalColorStrategy(background_color=background_color, tolerance=30)


@pytest.mark.parametrize(
    "tolerance",
    [
        -1,
        True,
        "30",
        None,
    ],
)
def test_global_color_strategy_rejects_invalid_tolerance(tolerance):
    with pytest.raises(InvalidToleranceError):
        GlobalColorStrategy(background_color=(255, 255, 255), tolerance=tolerance)
