import colorsys
from struct import Struct


class Color:

    __slots__ = ['red', 'green', 'blue', 'alpha']
    packer = Struct('BBBB')

    def __init__(self, red=0.0, green=0.0, blue=0.0, alpha=1.0):
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

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

    @property
    def saturation(self):
        '''Returns the Saturation in the HSB color space
            if you need more than one value from the HSB
            color space, you should call color.hsb instead

            Result interval: 0 <= Saturation <= 1.0
        '''
        _, s, _ = self.hsb
        return s

    @property
    def hue(self):
        '''Returns the Hue in the HSB color space
            if you need more than one value from the HSB
            color space, you should call color.hsb instead

            Result interval: 0 <= Hue <= 1.0
        '''
        h, _, _ = self.hsb
        return h

    @property
    def hex(self):
        'Returns a hex string representation like #FF0000FF for opaque red'
        return '#' + ''.join("%0.2X" % int(x * 255) for x in self.components)

    def write(self, writable):
        return writable.write(bytes(self))
