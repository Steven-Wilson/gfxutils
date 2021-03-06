import pytest

from . import Color


class MockWriter:

    def __init__(self):
        self.written = None

    def write(self, value):
        self.written = value


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


def test_components():
    'Confirms that components come out in RGBA order'
    color = Color(red=1, green=2, blue=3, alpha=4)
    for n, component in enumerate(color.components):
        assert n + 1 == component


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


def test_documentation():
    white = Color(red=1.0, green=1.0, blue=1.0)
    assert white.hex == '#FFFFFFFF'

    clear = Color(alpha=0.0)
    assert clear.hex == '#00000000'

    red = Color.from_hsb(hue=0.0, saturation=1.0, brightness=1.0)
    assert red.hex == '#FF0000FF'


def test_documentation_primary_colors():
    red = Color(red=1.0)
    assert red.hex == '#FF0000FF'

    green = Color(green=1.0)
    assert green.hex == '#00FF00FF'

    blue = Color(blue=1.0)
    assert blue.hex == '#0000FFFF'

    transparent_black = Color(alpha=0.5)
    assert transparent_black.hex == '#0000007F'


def test_documentation_equality():
    red1 = Color(red=1.0)
    red2 = Color.from_hsb(hue=0.0, saturation=1.0, brightness=1.0)
    assert red1 == red2


def test_documentation_bytes():
    green = Color(green=1.0, alpha=0.5)
    assert bytes(green) == b'\x00\xFF\x00\x7F'


def test_lighten():
    base = Color(0.0, 0.8, 0.0)
    overlay = Color(1.0, 0.5, 0.0)
    assert base.lighten(overlay) == Color(1.0, 0.8, 0.0)


def test_darken():
    base = Color(0.0, 0.8, 0.0)
    overlay = Color(1.0, 0.5, 0.0)
    assert base.darken(overlay) == Color(0.0, 0.5, 0.0)


def test_add():
    base = Color(0.0, 0.5, 0.0)
    overlay = Color(1.0, 0.5, 0.0, 0.5)
    assert base.add(overlay) == Color(0.5, 0.75, 0.0)


def test_subtract():
    base = Color(0.0, 0.5, 0.0)
    overlay = Color(1.0, 0.5, 0.0, 0.5)
    assert base.subtract(overlay) == Color(0.0, 0.25, 0.0)


def test_multiply():
    base = Color(0.0, 0.5, 0.0)
    overlay = Color(1.0, 0.5, 0.0, 0.5)
    assert base.multiply(overlay) == Color(0.0, 0.25, 0.0)


def test_divide():
    base = Color(0.0, 0.5, 1.0)
    overlay = Color(1.0, 0.5, 0.0, 0.5)
    assert base.divide(overlay) == Color(0.0, 1.0, 1.0)


def test_hue_description():
    assert Color.from_hsb(hue=0 / 12, saturation=1.0, brightness=1.0).hue_description == 'Red'
    assert Color.from_hsb(hue=1 / 12, saturation=1.0, brightness=1.0).hue_description == 'Orange'
    assert Color.from_hsb(hue=2 / 12, saturation=1.0, brightness=1.0).hue_description == 'Yellow'
    assert Color.from_hsb(hue=3 / 12, saturation=1.0, brightness=1.0).hue_description == 'Lime'
    assert Color.from_hsb(hue=4 / 12, saturation=1.0, brightness=1.0).hue_description == 'Green'
    assert Color.from_hsb(hue=5 / 12, saturation=1.0, brightness=1.0).hue_description == 'Teal'
    assert Color.from_hsb(hue=6 / 12, saturation=1.0, brightness=1.0).hue_description == 'Cyan'
    assert Color.from_hsb(hue=7 / 12, saturation=1.0, brightness=1.0).hue_description == 'Aqua'
    assert Color.from_hsb(hue=8 / 12, saturation=1.0, brightness=1.0).hue_description == 'Blue'
    assert Color.from_hsb(hue=9 / 12, saturation=1.0, brightness=1.0).hue_description == 'Purple'
    assert Color.from_hsb(hue=10 / 12, saturation=1.0, brightness=1.0).hue_description == 'Magenta'
    assert Color.from_hsb(hue=11 / 12, saturation=1.0, brightness=1.0).hue_description == 'Pink'
    assert Color.from_hsb(hue=11.9 / 12, saturation=1.0, brightness=1.0).hue_description == 'Red'


def test_brightness_description():
    assert Color.from_hsb(brightness=1.0).brightness_description == 'Bright'
    assert Color.from_hsb(brightness=0.5).brightness_description == ''
    assert Color.from_hsb(brightness=0.1).brightness_description == 'Dark'
    assert Color.from_hsb(brightness=0.0).brightness_description == 'Black'
    assert Color.from_hsb(brightness=0.002).brightness_description == 'Very Dark'


def test_saturation_description():
    assert Color.from_hsb(saturation=0.8, brightness=1.0).saturation_description == 'Vivid'
    assert Color.from_hsb(saturation=0.6, brightness=1.0).saturation_description == ''
    assert Color.from_hsb(saturation=0.4, brightness=1.0).saturation_description == 'Pastel'
    assert Color.from_hsb(saturation=0.2, brightness=1.0).saturation_description == 'Pastel'
    assert Color.from_hsb(saturation=0.0, brightness=1.0).saturation_description == 'Gray'


def test_description():
    assert Color().description == 'Black'
    assert Color.from_hsb(brightness=0.5).description == 'Gray'
    assert Color(red=1.0).description == 'Vivid Bright Red'
    assert Color(red=1.0, green=0.9, blue=0.8).description == 'Pastel Bright Orange'
    assert Color(red=1.0, green=0.8, blue=0.8).description == 'Pastel Bright Red'


def test_copy(cornflower):
    c = cornflower.copy
    assert c == cornflower
    assert c is not cornflower


def test_uint32():
    red = Color(red=1)
    assert red.uint32 == 0xFF0000FF
    green = Color(green=1)
    assert green.uint32 == 0x00FF00FF
    blue = Color(blue=1)
    assert blue.uint32 == 0x0000FFFF


def test_hue_set():
    blue = Color(blue=1)
    # set hue to red
    blue.hue = 0
    assert blue.hex == '#FF0000FF'


def test_difference():
    red = Color(red=1)
    blue = Color(blue=1)
    assert red.difference(blue) == blue.difference(red)
    assert red.difference(blue).uint32 == 0xFF00FFFF


def test_write(cornflower):
    writer = MockWriter()
    cornflower.write(writer)
    assert writer.written == bytes(cornflower)
