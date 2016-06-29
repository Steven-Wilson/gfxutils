from math import sqrt, sin, cos, radians, atan2, degrees, isclose

class Vector2D:
    '''Simple 2D vector type.
        Emulates numeric types
            - All numeric operators are component-wise
                except *, /, *=, and /=
                which are scalar multiply and divides

            Example:
                v1 = Vector2D(2, 3)
                v2 = Vector2D(3, 2)
                v3 = v1 ** v2
                print(v3) # => Vector2D(8, 9)
    '''

    __slots__ = ['x', 'y']

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def from_degrees_and_length(cls, angle, length):
        angle = radians(angle)
        x = cos(angle) * length
        y = sin(angle) * length
        return cls(x, y)

    @classmethod
    def from_radians_and_length(cls, angle, length):
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
        x = self.x
        y = self.y
        return sqrt(x * x + y * y)

    @length.setter
    def length(self, value):
        current = self.length
        self *= (value / current)

    @property
    def length_squared(self):
        x = self.x
        y = self.y
        return x * x + y * y

    def normalize(self):
        self /= self.length

    @property
    def normalized(self):
        return self / self.length

    @normalized.setter
    def normalized(self, value):
        self.radians = value.radians

    @property
    def degrees(self):
        return degrees(self.radians)

    @degrees.setter
    def degrees(self, value):
        self.radians = radians(value)

    @property
    def radians(self):
        return atan2(self.y, self.x)

    @radians.setter
    def radians(self, value):
        new_v = Vector2D.from_radians_and_length(value, self.length)
        self.x = new_v.x
        self.y = new_v.y

    @property
    def copy(self):
        return Vector2D(self.x, self.y)
