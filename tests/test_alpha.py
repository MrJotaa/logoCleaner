import numpy as np

from logocleaner.masks.alpha import apply_transparency_mask


def test_apply_transparency_mask_sets_background_alpha_to_zero():
    image = np.full((2, 2, 4), [255, 0, 0, 255], dtype=np.uint8)
    mask = np.array(
        [
            [True, False],
            [False, True],
        ],
        dtype=np.bool_,
    )

    result = apply_transparency_mask(image, mask)

    assert result[0, 0, 3] == 0
    assert result[0, 1, 3] == 255
    assert result[1, 0, 3] == 255
    assert result[1, 1, 3] == 0


def test_apply_transparency_mask_does_not_mutate_input_image():
    image = np.full((2, 2, 4), [255, 0, 0, 255], dtype=np.uint8)
    original = image.copy()
    mask = np.ones((2, 2), dtype=np.bool_)

    apply_transparency_mask(image, mask)

    np.testing.assert_array_equal(image, original)
