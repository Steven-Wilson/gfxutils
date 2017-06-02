import colorsys
from struct import Struct

__all__ = ['Color']


class Color:

    __slots__ = ['red', 'green', 'blue', 'alpha']

    # NOTE: Even though we store these as floats between 0 and 1 in python
    #       When we write this out to binary, we encode it as 4 bytes RGBA.
    #       This will lose precision, but most displays have this as their
    #       native pixel format, So the 4x space cost seems worthwhile
    #       since you're most likely Looking to save space if using binary
    packer = Struct('BBBB')

    def __init__(self, red=0.0, green=0.0, blue=0.0, alpha=1.0):
        self.red = float(red)
        self.green = float(green)
        self.blue = float(blue)
        self.alpha = float(alpha)

    @property
    def copy(self):
        return Color(self.red, self.green, self.blue, self.alpha)

    @property
    def uint32(self):
        return int(self.red * 255) << 24 | int(self.green * 255) << 16 | int(self.blue * 255) << 8 | int(self.alpha * 255)

    @property
    def rgba8888(self):
        return int(self.red * 255), int(self.green * 255), int(self.blue * 255), int(self.alpha * 255)

    @classmethod
    def from_bytes(cls, packed_bytes):
        components = cls.packer.unpack(packed_bytes)
        red, green, blue, alpha = [x / 255 for x in components]
        return cls(red, green, blue, alpha)

    @classmethod
    def from_hsb(cls, hue=0.0, saturation=0.0, brightness=0.0, alpha=1.0):
        r, g, b = colorsys.hsv_to_rgb(hue, saturation, brightness)
        return cls(red=r, green=g, blue=b, alpha=alpha)

    def __repr__(self):
        template = '{}({:.3f}, {:.3f}, {:.3f}, {:.3f})'
        return template.format(self.__class__.__name__,
                               self.red, self.green, self.blue, self.alpha)

    def __bytes__(self):
        red, green, blue, alpha = [int(x * 255) for x in self.components]
        return self.packer.pack(red, green, blue, alpha)

    def __bool__(self):
        return True

    @property
    def components(self):
        'Returns a tuple of the component channels in RGBA order'
        return self.red, self.green, self.blue, self.alpha

    def __eq__(self, other):
        for a, b in zip(self.components, other.components):
            if abs(a - b) > 0.01:
                return False
        else:
            return True

    def blend(self, other):
        '''Blends current color together with another color, using
            the alpha from the other color for composition
        '''
        alpha = other.alpha
        red = self.red * (1 - alpha) + other.red * alpha
        green = self.green * (1 - alpha) + other.green * alpha
        blue = self.blue * (1 - alpha) + other.blue * alpha
        return self.__class__(red, green, blue, self.alpha)

    @property
    def hsb(self):
        'Returns a Hue, Saturation, Brightness tuple'
        return colorsys.rgb_to_hsv(self.red, self.green, self.blue)

    @hsb.setter
    def hsb(self, values):
        'Sets the Hue, Saturation, Brightness tuple'
        self.red, self.green, self.blue = colorsys.hsv_to_rgb(*values)

    @property
    def brightness(self):
        '''Returns the Brightness in the HSB color space
            if you need more than one value from the HSB
            color space, you should call color.hsb instead

            Result interval: 0 <= Brightness <= 1.0
        '''
        _, _, b = self.hsb
        return b

    @brightness.setter
    def brightness(self, other):
        # Bound between 0 and 1
        if other > 1:
            other = 1
        elif other < 0:
            other = 0
        h, s, _ = self.hsb
        self.red, self.green, self.blue = colorsys.hsv_to_rgb(h, s, other)

    @property
    def saturation(self):
        '''Returns the Saturation in the HSB color space
            if you need more than one value from the HSB
            color space, you should call color.hsb instead

            Result interval: 0 <= Saturation <= 1.0
        '''
        _, s, _ = self.hsb
        return s

    @saturation.setter
    def saturation(self, other):
        # Bound between 0 and 1
        if other > 1:
            other = 1
        elif other < 0:
            other = 0
        h, _, b = self.hsb
        self.red, self.green, self.blue = colorsys.hsv_to_rgb(h, other, b)


    @property
    def hue(self):
        '''Returns the Hue in the HSB color space
            if you need more than one value from the HSB
            color space, you should call color.hsb instead

            Result interval: 0 <= Hue <= 1.0
        '''
        h, _, _ = self.hsb
        return h

    @hue.setter
    def hue(self, other):
        # Bound between 0 and 1 on a repeating period
        other = other - (other // 1)
        _, s, b = self.hsb
        self.red, self.green, self.blue = colorsys.hsv_to_rgb(other, s, b)

    @property
    def hex(self):
        'Returns a hex string representation like #FF0000FF for opaque red'
        return '#' + ''.join("%0.2X" % int(x * 255) for x in self.components)

    def write(self, writable):
        return writable.write(bytes(self))

    def lighten(self, other):
        alpha = max(self.alpha, other.alpha)
        red = max(self.red, other.red)
        green = max(self.green, other.green)
        blue = max(self.blue, other.blue)
        return self.__class__(red, green, blue, alpha)

    def darken(self, other):
        alpha = min(self.alpha, other.alpha)
        red = min(self.red, other.red)
        green = min(self.green, other.green)
        blue = min(self.blue, other.blue)
        return self.__class__(red, green, blue, alpha)

    def add(self, other):
        red = min(self.red + other.red * other.alpha, 1.0)
        green = min(self.green + other.green * other.alpha, 1.0)
        blue = min(self.blue + other.blue * other.alpha, 1.0)
        return self.__class__(red, green, blue, self.alpha)

    def subtract(self, other):
        red = max(self.red - other.red * other.alpha, 0.0)
        green = max(self.green - other.green * other.alpha, 0.0)
        blue = max(self.blue - other.blue * other.alpha, 0.0)
        return self.__class__(red, green, blue, self.alpha)

    def multiply(self, other):
        red = min(self.red * other.red, 1.0)
        green = min(self.green * other.green, 1.0)
        blue = min(self.blue * other.blue, 1.0)
        return self.__class__(red, green, blue, self.alpha)

    def divide(self, other):
        red = 1.0 if other.red == 0 else self.red / other.red
        green = 1.0 if other.green == 0 else self.green / other.green
        blue = 1.0 if other.blue == 0 else self.blue / other.blue
        return self.__class__(red, green, blue, self.alpha)

    def difference(self, other):
        red = abs(self.red - other.red)
        green = abs(self.green - other.green)
        blue = abs(self.blue - other.blue)
        return self.__class__(red, green, blue, self.alpha)

    @property
    def hue_description(self):
        hue = self.hue
        if hue < 1 / 24:
            return 'Red'
        elif hue < 3 / 24:
            return 'Orange'
        elif hue < 5 / 24:
            return 'Yellow'
        elif hue < 7 / 24:
            return 'Lime'
        elif hue < 9 / 24:
            return 'Green'
        elif hue < 11 / 24:
            return 'Teal'
        elif hue < 13 / 24:
            return 'Cyan'
        elif hue < 15 / 24:
            return 'Aqua'
        elif hue < 17 / 24:
            return 'Blue'
        elif hue < 19 / 24:
            return 'Purple'
        elif hue < 21 / 24:
            return 'Magenta'
        elif hue < 23 / 24:
            return 'Pink'
        else:
            return 'Red'

    @property
    def brightness_description(self):
        brightness = self.brightness
        if brightness > 0.8:
            return 'Bright'
        elif brightness > 0.2:
            return ''
        elif brightness > 0.05:
            return 'Dark'
        elif brightness < 0.001:
            return 'Black'
        else:
            return 'Very Dark'

    @property
    def saturation_description(self):
        saturation = self.saturation
        if saturation > 0.75:
            return 'Vivid'
        elif saturation > 0.5:
            return ''
        elif saturation > 0.1:
            return 'Pastel'
        else:
            return 'Gray'

    @property
    def description(self):
        brightness = self.brightness_description
        if brightness == 'Black':
            return 'Black'
        hue = self.hue_description
        saturation = self.saturation_description
        if saturation == 'Gray':
            hue = 'Gray'
            saturation = ''
        descriptions = [saturation, brightness, hue]
        descriptions = [d for d in descriptions if d != '']
        return ' '.join(descriptions)
