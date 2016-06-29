from .vector import Vector2D


class Box2D:

    def __init__(self, position, size, origin=None, rotation=0):
        if abs(size) != size:
            raise ValueError("size must be strictly positive")
        if origin is None:
            origin = Vector2D(0, 0)
        self.position = position
        self.origin = origin
        self.size = size
        self.rotation = rotation

    @property
    def top_left(self):
        origin = self.origin
        result = Vector2D(-origin.x, self.size.y - origin.y)
        result.radians += self.rotation
        result += self.position
        return result

    @property
    def top_right(self):
        origin = self.origin
        size = self.size
        result = Vector2D(size.x - origin.x, size.y - origin.y)
        result.radians += self.rotation
        result += self.position
        return result

    @property
    def bottom_left(self):
        origin = self.origin
        result = Vector2D(-origin.x, -origin.y)
        result.radians += self.rotation
        result += self.position
        return result

    @property
    def bottom_right(self):
        origin = self.origin
        size = self.size
        result = Vector2D(size.x - origin.x, -origin.y)
        result.radians += self.rotation
        result += self.position
        return result

    @property
    def center(self):
        return self.position + self.size / 2 - self.origin

    @property
    def area(self):
        return self.size.x * self.size.y

    @property
    def points(self):
        yield self.top_left
        yield self.top_right
        yield self.bottom_right
        yield self.bottom_left
