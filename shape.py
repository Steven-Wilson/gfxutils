from .vector import V2
from struct import Struct


__all__ = ['Circle', 'Rect']

pi = 3.14159265358979323846264


class Circle:

    __slots__ = ['radius', 'position']
    packer = Struct('d')

    def __init__(self, radius=1.0, position=None):
        self.radius = float(radius)
        if not position:
            self.position = V2(0, 0)
        else:
            self.position = position

    @classmethod
    def from_bytes(cls, packed_bytes):
        radius = cls.packer.unpack(packed_bytes[:8])[0]
        position = V2.from_bytes(packed_bytes[8:])
        return cls(radius=radius, position=position)

    @property
    def area(self):
        return self.radius * self.radius * pi

    @property
    def diameter(self):
        return self.radius * 2

    def contains(self, point):
        return (self.position - point).length < self.radius

    def translate(self, vector):
        self.position += vector

    def scale(self, factor):
        self.radius *= factor

    def __bytes__(self):
        return self.packer.pack(self.radius) + bytes(self.position)

    def __eq__(self, other):
        return self.radius == other.radius and self.position == other.position

    def write(self, writable):
        return writable.write(bytes(self))


class Rect:

    __slots__ = ['position', 'size']

    def __init__(self, position=None, size=None):
        if position is None:
            self.position = V2(0, 0)
        else:
            self.position = position

        if size is None:
            self.size = V2(0, 0)
        else:
            self.size = size

    @classmethod
    def from_bytes(cls, packed_bytes):
        position = V2.from_bytes(packed_bytes[:16])
        size = V2.from_bytes(packed_bytes[16:])
        return cls(position=position, size=size)

    def __bytes__(self):
        return bytes(self.position) + bytes(self.size)

    def __eq__(self, other):
        if self.position != other.position:
            return False
        if self.size != other.size:
            return False
        return True

    @property
    def width(self):
        return self.size.x

    @property
    def height(self):
        return self.size.y

    @property
    def x(self):
        return self.position.x

    @property
    def y(self):
        return self.position.y

    @property
    def area(self):
        return self.width * self.height

    @property
    def perimeter(self):
        return self.width * 2 + self.height * 2

    @property
    def x1(self):
        return self.position.x

    @property
    def y1(self):
        return self.position.y

    @property
    def x2(self):
        return self.position.x + self.size.x

    @property
    def y2(self):
        return self.position.y + self.size.y

    def contains(self, point):
        if point.x >= self.x and point.x < self.x2:
            if point.y >= self.y and point.y < self.y2:
                return True
        return False

    def translate(self, vector):
        self.position += vector

    def scale(self, factor):
        self.size *= factor


class Line:

    __slots__ = ['p1', 'p2']

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    @property
    def length(self):
        return (self.p2 - self.p1).length

    def intersection(self, other):
        d1 = self.p2 - self.p1
        d2 = other.p2 - other.p1
        try:
            m1 = (d1.y / d1.x)
            m2 = (d2.y / d2.x)
            b1 = - m1 * self.p1.x
            b2 = - m2 * self.p2.x
            x = (b2 - b1) / (m1 - m2)
            y = m1 * x + b1
            return V2(x, y)
        except ZeroDivisionError:
            raise NotImplementedError('Axis-aligned lines not yet supported')
