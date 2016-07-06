import pytest
from color import Color


@pytest.fixture
def cornflower():
    return Color(red=0.478, green=0.671, blue=0.890, alpha=1.0)


def test_defaults():
    color = Color()
    assert color.red == 0.0
    assert color.blue == 0.0
    assert color.green == 0.0
    assert color.alpha == 1.0


def test_default_repr():
    color = Color()
    assert repr(color) == "Color(0.000, 0.000, 0.000, 1.000)"


def test_red_repr():
    color = Color(red=1.0)
    assert repr(color) == "Color(1.000, 0.000, 0.000, 1.000)"


def test_green_repr():
    color = Color(green=1.0)
    assert repr(color) == "Color(0.000, 1.000, 0.000, 1.000)"


def test_blue_repr():
    color = Color(blue=1.0)
    assert repr(color) == "Color(0.000, 0.000, 1.000, 1.000)"


def test_alpha_repr():
    color = Color(alpha=0.0)
    assert repr(color) == "Color(0.000, 0.000, 0.000, 0.000)"


# def test_components():
#     color = Color(red=1, green=2, blue=3, alpha=4)
#     for n, component in enumerate(color.components):
#         assert n + 1 == component

def test_bool():
    assert Color()


def test_equals():
    a = Color(red=0.10, green=0.15, blue=0.30)
    b = Color(red=0.10, green=0.15, blue=0.30)
    assert a == b


def test_not_equals():
    a = Color(red=0.10, green=0.15, blue=0.30)
    b = Color(red=0.10, green=0.12, blue=0.30)
    assert a != b


def test_bytes(cornflower):
    packed_bytes = bytes(cornflower)
    c = Color.from_bytes(packed_bytes)
    assert cornflower == c


def test_blend():
    black = Color()
    white = Color(red=1.0, green=1.0, blue=1.0, alpha=0.5)
    gray = black.blend(white)
    assert gray.red == 0.5
    assert gray.green == 0.5
    assert gray.blue == 0.5
    assert gray.alpha == 1.0


def test_brightness():
    black = Color()
    assert black.brightness == 0.0

    white = Color(red=1.0, green=1.0, blue=1.0)
    assert white.brightness == 1.0

    white = Color(red=0.5, green=0.5, blue=0.5)
    assert white.brightness == 0.5


def test_set_hsb():
    color = Color()
    color.hsb = (0.0, 1.0, 1.0)

    assert color.red == 1.0
    assert color.green == 0.0
    assert color.blue == 0.0


def test_saturation():
    color = Color(red=1.0)
    assert color.saturation == 1.0

    color = Color(red=0.5, green=0.6, blue=0.5)
    assert color.saturation < 1.0

    color = Color()
    assert color.saturation == 0.0


def test_hue():
    color = Color(red=1.0)
    assert color.hue == 0.0

    color = Color(green=1.0)
    assert abs(color.hue - 0.33333) < 0.001

    color = Color(blue=1.0)
    assert abs(color.hue - 0.66666) < 0.001


def test_hsb_constructor():
    red = Color.from_hsb(hue=0.0, saturation=1.0, brightness=1.0)
    assert red == Color(red=1.0)


def test_hex_code():
    red = Color(red=1.0)
    green = Color(green=1.0)
    blue = Color(blue=1.0)
    transparent_black = Color(alpha=0.5)
    assert red.hex == '#FF0000FF'
    assert green.hex == '#00FF00FF'
    assert blue.hex == '#0000FFFF'
    assert transparent_black.hex == '#0000007F'


def test_packed_size():
    b = bytes(Color())
    assert len(b) == 4
