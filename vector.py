from math import sqrt, sin, cos, radians, atan2, degrees, isclose


class Vector2D:
    'Simple 2D vector type that does what you expect (mostly)'

    __slots__ = ['x', 'y']

    def __init__(self, x, y):
        'Most efficient way to make a vector: from x and y'
        self.x = x
        self.y = y

    @classmethod
    def from_degrees_and_length(cls, angle, length):
        'Creates a new vector from an angle in degress and a length'
        angle = radians(angle)
        x = cos(angle) * length
        y = sin(angle) * length
        return cls(x, y)

    @classmethod
    def from_radians_and_length(cls, angle, length):
        'Creates a new vector from an angle in radians and a length'
        x = cos(angle) * length
        y = sin(angle) * length
        return cls(x, y)

    def __repr__(self):
        return "Vector2D({:.3f}, {:.3f})".format(self.x, self.y)

    def __bytes__(self):
        raise NotImplementedError("TODO")

    def __add__(self, other):
        return Vector2D(self.x + other.x,
                        self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x,
                        self.y - other.y)

    def __mul__(self, other):
        return Vector2D(self.x * other,
                        self.y * other)

    def __truediv__(self, other):
        return Vector2D(self.x / other,
                        self.y / other)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        return self

    def __itruediv__(self, other):
        self.x /= other
        self.y /= other
        return self

    def __neg__(self):
        return Vector2D(-self.x, -self.y)

    def __pos__(self):
        return Vector2D(+self.x, +self.y)

    def __abs__(self):
        return Vector2D(abs(self.x), abs(self.y))

    def __eq__(self, other):
        return isclose((self - other).length, 0,
                       rel_tol=0.0001, abs_tol=0.00001)

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        'TODO: Improve hashing function'
        return hash(hash(self.x) + hash(self.y))

    def __bool__(self):
        'Any truth-checks against vectors will pass'
        return True

    def __getitem__(self, key):
        '''Allows vec[0] to provide the x component
            and vec[1] to provide the y component'''
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            message = "Cannot get the {}th item".format(key)
            raise IndexError("2D Vectors only have 2 components, " + message)

    def __setitem__(self, key, value):
        '''Allows vec[0] = x to set the x component
            and vec[1] = y to set the y component'''
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            message = "Cannot set the {}th item".format(key)
            raise IndexError("2D Vectors only have 2 components, " + message)

    def __delitem__(self, key):
        raise NotImplementedError("Cannot remove a component from a Vector2D")

    def __iter__(self):
        yield self.x
        yield self.y

    def __reversed__(self):
        yield self.y
        yield self.x

    def __contains__(self, item):
        'Returns true if either component matches the item'
        return isclose(item, self.x, rel_tol=0.0001, abs_tol=0.00001) or \
            isclose(item, self.y, rel_tol=0.0001, abs_tol=0.00001)

    @property
    def length(self):
        'The magnitude of the vector'
        x = self.x
        y = self.y
        return sqrt(x * x + y * y)

    @length.setter
    def length(self, value):
        'Sets the magnitude of the vector'
        current = self.length
        self *= (value / current)

    @property
    def length_squared(self):
        'The squared magnitude of the vector.  Fast for length compares'
        x = self.x
        y = self.y
        return x * x + y * y

    def normalize(self):
        'Grows or Shrinks the vector to a size of 1.0 but maintains angle'
        self.length = 1

    @property
    def normalized(self):
        'Returns a normalized copy of the vector'
        return self / self.length

    @normalized.setter
    def normalized(self, value):
        '''Ensures the vector, when normalized, will match the normalized
            version of the vector povided'''
        self.radians = value.radians

    @property
    def degrees(self):
        'Returns the angle of the vector in degrees'
        return degrees(self.radians)

    @degrees.setter
    def degrees(self, value):
        'Sets the angle of the vector in degrees'
        self.radians = radians(value)

    @property
    def radians(self):
        'Returns the angle of the vector in radians'
        return atan2(self.y, self.x)

    @radians.setter
    def radians(self, value):
        'Sets the angle of the vector in radians'
        new_v = Vector2D.from_radians_and_length(value, self.length)
        self.x = new_v.x
        self.y = new_v.y

    @property
    def copy(self):
        'Makes a copy of the vector'
        return Vector2D(self.x, self.y)

    def dot_product(self, other):
        'Returns the dot product'
        return self.x * other.x + self.y * other.y
