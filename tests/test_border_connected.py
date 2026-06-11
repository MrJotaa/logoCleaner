import numpy as np
import pytest

from logocleaner.exceptions import InvalidColorError, InvalidToleranceError
from logocleaner.strategies.base import BackgroundRemovalStrategy, validate_strategy_mask
from logocleaner.strategies.border_connected import BorderConnectedStrategy


def test_border_connected_strategy_matches_strategy_interface():
    strategy = BorderConnectedStrategy(background_color=(255, 255, 255), tolerance=30)

    assert isinstance(strategy, BackgroundRemovalStrategy)


def test_border_connected_strategy_has_name():
    strategy = BorderConnectedStrategy(background_color=(255, 255, 255), tolerance=30)

    assert strategy.name == "border"


def test_border_connected_strategy_removes_background_connected_to_border():
    image = np.full((5, 5, 4), [255, 255, 255, 255], dtype=np.uint8)
    image[2, 2] = [255, 0, 0, 255]

    strategy = BorderConnectedStrategy(background_color=(255, 255, 255), tolerance=0)

    mask = strategy.create_mask(image)

    expected_mask = np.array(
        [
            [True, True, True, True, True],
            [True, True, True, True, True],
            [True, True, False, True, True],
            [True, True, True, True, True],
            [True, True, True, True, True],
        ],
        dtype=np.bool_,
    )

    np.testing.assert_array_equal(mask, expected_mask)
    validate_strategy_mask(mask, image)


def test_border_connected_strategy_preserves_internal_background_colored_holes():
    image = np.full((7, 7, 4), [255, 255, 255, 255], dtype=np.uint8)

    red = [255, 0, 0, 255]

    image[2, 2:5] = red
    image[4, 2:5] = red
    image[2:5, 2] = red
    image[2:5, 4] = red

    strategy = BorderConnectedStrategy(background_color=(255, 255, 255), tolerance=0)

    mask = strategy.create_mask(image)

    expected_mask = np.array(
        [
            [True, True, True, True, True, True, True],
            [True, True, True, True, True, True, True],
            [True, True, False, False, False, True, True],
            [True, True, False, False, False, True, True],
            [True, True, False, False, False, True, True],
            [True, True, True, True, True, True, True],
            [True, True, True, True, True, True, True],
        ],
        dtype=np.bool_,
    )

    np.testing.assert_array_equal(mask, expected_mask)


def test_border_connected_strategy_uses_tolerance_only_for_connected_pixels():
    image = np.array(
        [
            [[255, 255, 255, 255], [250, 250, 250, 255], [255, 255, 255, 255]],
            [[255, 0, 0, 255], [250, 250, 250, 255], [255, 0, 0, 255]],
            [[255, 0, 0, 255], [255, 0, 0, 255], [255, 0, 0, 255]],
        ],
        dtype=np.uint8,
    )

    strategy = BorderConnectedStrategy(background_color=(255, 255, 255), tolerance=10)

    mask = strategy.create_mask(image)

    expected_mask = np.array(
        [
            [True, True, True],
            [False, True, False],
            [False, False, False],
        ],
        dtype=np.bool_,
    )

    np.testing.assert_array_equal(mask, expected_mask)


def test_border_connected_strategy_does_not_remove_unconnected_matching_pixels():
    image = np.full((5, 5, 4), [255, 0, 0, 255], dtype=np.uint8)

    image[0, :] = [255, 255, 255, 255]
    image[2, 2] = [255, 255, 255, 255]

    strategy = BorderConnectedStrategy(background_color=(255, 255, 255), tolerance=0)

    mask = strategy.create_mask(image)

    expected_mask = np.array(
        [
            [True, True, True, True, True],
            [False, False, False, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False],
        ],
        dtype=np.bool_,
    )

    np.testing.assert_array_equal(mask, expected_mask)


def test_border_connected_strategy_returns_boolean_mask_matching_image_shape():
    image = np.full((10, 20, 4), [255, 255, 255, 255], dtype=np.uint8)

    strategy = BorderConnectedStrategy(background_color=(255, 255, 255), tolerance=30)

    mask = strategy.create_mask(image)

    assert mask.dtype == np.bool_
    assert mask.shape == (10, 20)


def test_border_connected_strategy_does_not_mutate_input_image():
    image = np.full((3, 3, 4), [255, 255, 255, 255], dtype=np.uint8)
    original = image.copy()

    strategy = BorderConnectedStrategy(background_color=(255, 255, 255), tolerance=30)
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
def test_border_connected_strategy_rejects_invalid_background_color(background_color):
    with pytest.raises(InvalidColorError):
        BorderConnectedStrategy(background_color=background_color, tolerance=30)


@pytest.mark.parametrize(
    "tolerance",
    [
        -1,
        True,
        "30",
        None,
        float("inf"),
        float("nan"),
    ],
)
def test_border_connected_strategy_rejects_invalid_tolerance(tolerance):
    with pytest.raises(InvalidToleranceError):
        BorderConnectedStrategy(background_color=(255, 255, 255), tolerance=tolerance)
