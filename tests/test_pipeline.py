import numpy as np
from PIL import Image

from logocleaner.core.pipeline import clean_background
from logocleaner.strategies.global_color import GlobalColorStrategy


def test_clean_background_applies_strategy_mask_to_image_alpha():
    image_array = np.full((3, 3, 4), [255, 255, 255, 255], dtype=np.uint8)
    image_array[1, 1] = [255, 0, 0, 255]

    image = Image.fromarray(image_array, mode="RGBA")
    strategy = GlobalColorStrategy(background_color=(255, 255, 255), tolerance=0)

    result = clean_background(image, strategy)

    result_array = np.asarray(result.image)

    assert result_array[0, 0, 3] == 0
    assert result_array[1, 1, 3] == 255
    assert result.background_mask.shape == (3, 3)
    assert result.background_mask[0, 0]
    assert not result.background_mask[1, 1]


def test_clean_background_does_not_mutate_original_image():
    image_array = np.full((3, 3, 4), [255, 255, 255, 255], dtype=np.uint8)
    image = Image.fromarray(image_array.copy(), mode="RGBA")
    original = np.asarray(image).copy()

    strategy = GlobalColorStrategy(background_color=(255, 255, 255), tolerance=0)
    clean_background(image, strategy)

    np.testing.assert_array_equal(np.asarray(image), original)
