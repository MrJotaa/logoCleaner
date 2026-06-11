import numpy as np
import pytest

from logocleaner.background.detect import detect_background_color
from logocleaner.exceptions import BackgroundColorDetectionError


def test_detect_background_color_from_uniform_white_image():
    image = np.full((10, 10, 4), [255, 255, 255, 255], dtype=np.uint8)

    assert detect_background_color(image) == (255, 255, 255)


def test_detect_background_color_uses_border_not_center():
    image = np.full((10, 10, 4), [255, 255, 255, 255], dtype=np.uint8)
    image[3:7, 3:7] = [255, 0, 0, 255]

    assert detect_background_color(image) == (255, 255, 255)


def test_detect_background_color_is_robust_to_small_border_contamination():
    image = np.full((10, 10, 4), [255, 255, 255, 255], dtype=np.uint8)

    image[0, 0] = [0, 0, 0, 255]
    image[0, 1] = [0, 0, 0, 255]

    assert detect_background_color(image) == (255, 255, 255)


def test_detect_background_color_can_use_larger_border_width():
    image = np.full((20, 20, 4), [240, 240, 240, 255], dtype=np.uint8)
    image[5:15, 5:15] = [0, 0, 255, 255]

    assert detect_background_color(image, border_width=2) == (240, 240, 240)


def test_detect_background_color_ignores_transparent_border_pixels():
    image = np.full((10, 10, 4), [0, 0, 0, 0], dtype=np.uint8)

    image[0, :] = [255, 255, 255, 255]
    image[-1, :] = [255, 255, 255, 255]

    assert detect_background_color(image) == (255, 255, 255)


def test_detect_background_color_fails_when_no_visible_border_pixels_exist():
    image = np.full((10, 10, 4), [255, 255, 255, 0], dtype=np.uint8)

    with pytest.raises(BackgroundColorDetectionError):
        detect_background_color(image)


def test_detect_background_color_rejects_non_rgba_image():
    image = np.zeros((10, 10, 3), dtype=np.uint8)

    with pytest.raises(BackgroundColorDetectionError):
        detect_background_color(image)


def test_detect_background_color_rejects_empty_image():
    image = np.zeros((0, 10, 4), dtype=np.uint8)

    with pytest.raises(BackgroundColorDetectionError):
        detect_background_color(image)


@pytest.mark.parametrize("border_width", [0, -1, 1.5, True])
def test_detect_background_color_rejects_invalid_border_width(border_width):
    image = np.full((10, 10, 4), [255, 255, 255, 255], dtype=np.uint8)

    with pytest.raises(BackgroundColorDetectionError):
        detect_background_color(image, border_width=border_width)


def test_detect_background_color_rejects_border_width_larger_than_image():
    image = np.full((10, 10, 4), [255, 255, 255, 255], dtype=np.uint8)

    with pytest.raises(BackgroundColorDetectionError):
        detect_background_color(image, border_width=11)


@pytest.mark.parametrize("min_alpha", [-1, 256, 1.5, True])
def test_detect_background_color_rejects_invalid_min_alpha(min_alpha):
    image = np.full((10, 10, 4), [255, 255, 255, 255], dtype=np.uint8)

    with pytest.raises(BackgroundColorDetectionError):
        detect_background_color(image, min_alpha=min_alpha)
