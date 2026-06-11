import numpy as np
import pytest

from logocleaner.core.colors import (
    color_distance,
    create_color_distance_map,
    parse_hex_color,
    validate_rgb_color,
)
from logocleaner.exceptions import InvalidColorError


def test_parse_hex_color_accepts_valid_color():
    assert parse_hex_color("#ffffff") == (255, 255, 255)
    assert parse_hex_color("#000000") == (0, 0, 0)
    assert parse_hex_color("#ff0000") == (255, 0, 0)
    assert parse_hex_color("#00AAff") == (0, 170, 255)


@pytest.mark.parametrize(
    "value",
    [
        "",
        "ffffff",
        "#fff",
        "#fffffff",
        "#gggggg",
        "red",
    ],
)
def test_parse_hex_color_rejects_invalid_values(value):
    with pytest.raises(InvalidColorError):
        parse_hex_color(value)


def test_validate_rgb_color_accepts_valid_rgb_color():
    assert validate_rgb_color((0, 128, 255)) == (0, 128, 255)


@pytest.mark.parametrize(
    "color",
    [
        (-1, 0, 0),
        (0, 256, 0),
        (0, 0, 999),
    ],
)
def test_validate_rgb_color_rejects_out_of_range_channels(color):
    with pytest.raises(InvalidColorError):
        validate_rgb_color(color)


def test_color_distance_returns_zero_for_same_color():
    assert color_distance((255, 255, 255), (255, 255, 255)) == 0


def test_color_distance_calculates_rgb_euclidean_distance():
    assert color_distance((255, 255, 255), (0, 0, 0)) == pytest.approx(441.6729, rel=1e-4)


def test_create_color_distance_map_returns_distance_per_pixel():
    image = np.array(
        [
            [[255, 255, 255, 255], [0, 0, 0, 255]],
            [[250, 250, 250, 255], [255, 0, 0, 255]],
        ],
        dtype=np.uint8,
    )

    distance_map = create_color_distance_map(image, (255, 255, 255))

    assert distance_map.shape == (2, 2)
    assert distance_map.dtype == np.float32
    assert distance_map[0, 0] == 0
    assert distance_map[0, 1] == pytest.approx(441.6729, rel=1e-4)
    assert distance_map[1, 0] == pytest.approx(8.6602, rel=1e-4)
    assert distance_map[1, 1] == pytest.approx(360.6244, rel=1e-4)


def test_create_color_distance_map_rejects_non_rgba_image():
    image = np.zeros((10, 10, 3), dtype=np.uint8)

    with pytest.raises(InvalidColorError):
        create_color_distance_map(image, (255, 255, 255))


def test_validate_rgb_color_accepts_list_rgb_color():
    assert validate_rgb_color([0, 128, 255]) == (0, 128, 255)


def test_validate_rgb_color_accepts_numpy_integer_channels():
    assert validate_rgb_color((np.uint8(255), np.uint8(128), np.uint8(0))) == (255, 128, 0)


@pytest.mark.parametrize(
    "color",
    [
        None,
        123,
        object(),
        "ffffff",
        b"ffffff",
        (255, 255),
        (255, 255, 255, 255),
        (255.0, 0, 0),
        (True, 0, 0),
    ],
)
def test_validate_rgb_color_rejects_invalid_color_shapes_or_types(color):
    with pytest.raises(InvalidColorError):
        validate_rgb_color(color)
