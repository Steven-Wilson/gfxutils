from vector import Vector
from struct import Struct


pi = 3.14159265358979323846264


class Circle:

    __slots__ = ['radius', 'position']
    packer = Struct('d')

    def __init__(self, radius=1.0, position=None):
        self.radius = float(radius)
        if not position:
            self.position = Vector(0, 0)
        else:
            self.position = position

    @classmethod
    def from_bytes(cls, packed_bytes):
        radius = cls.packer.unpack(packed_bytes[:8])[0]
        position = Vector.from_bytes(packed_bytes[8:])
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
