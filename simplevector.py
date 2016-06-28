from sys import float_info
from math import sqrt, sin, cos, radians, atan2, degrees


epsilon = float_info.epsilon * 100


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

    def __mod__(self, other):
        return Vector2D(self.x % other.x,
                        self.y % other.y)

    def __divmod__(self, other):
        raise NotImplementedError("divmod makes no sense on Vectors")

    def __pow__(self, other):
        return Vector2D(self.x ** other.x,
                        self.y ** other.y)

    def __lshift__(self, other):
        return Vector2D(self.x << other.x,
                        self.y << other.y)

    def __rshift__(self, other):
        return Vector2D(self.x >> other.x,
                        self.y >> other.y)

    def __and__(self, other):
        return Vector2D(self.x & other.x,
                        self.y & other.y)

    def __xor__(self, other):
        return Vector2D(self.x ^ other.x,
                        self.y ^ other.y)

    def __or__(self, other):
        return Vector2D(self.x | other.x,
                        self.y | other.y)

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

    def __imod__(self, other):
        self.x %= other.x
        self.y %= other.y
        return self

    def __idivmod__(self, other):
        raise NotImplementedError("divmod makes no sense on Vectors")

    def __ipow__(self, other):
        self.x **= other.x
        self.y **= other.y
        return self

    def __ilshift__(self, other):
        self.x <<= other.x
        self.y <<= other.y
        return self

    def __irshift__(self, other):
        self.x >>= other.x
        self.y >>= other.y
        return self

    def __iand__(self, other):
        self.x &= other.x
        self.y &= other.y
        return self

    def __ixor__(self, other):
        self.x ^= other.x
        self.y ^= other.y
        return self

    def __ior__(self, other):
        self.x |= other.x
        self.y |= other.y
        return self

    def __neg__(self):
        return Vector2D(-self.x, -self.y)

    def __pos__(self):
        return Vector2D(+self.x, +self.y)

    def __abs__(self):
        return Vector2D(abs(self.x), abs(self.y))

    def __invert__(self):
        return Vector2D(~self.x, ~self.y)

    def __lt__(self, other):
        response = "Unintelligible Expression: {} < {}".format(self, other)
        raise NotImplementedError(response)

    def __gt__(self, other):
        response = "Unintelligible Expression: {} > {}".format(self, other)
        raise NotImplementedError(response)

    def __le__(self, other):
        response = "Unintelligible Expression: {} <= {}".format(self, other)
        raise NotImplementedError(response)

    def __ge__(self, other):
        response = "Unintelligible Expression: {} >= {}".format(self, other)
        raise NotImplementedError(response)

    def __eq__(self, other):
        return (self - other).length < epsilon

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        'TODO: Improve hashing function'
        return hash(hash(self.x) + hash(self.y))

    def __bool__(self):
        'Any truth-checks against vectors will pass'
        return True

    def __len__(self):
        raise NotImplementedError("Python wouldn't let me return float ;(")

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
        return item == self.x or item == self.y

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

    @property
    def degrees(self):
        return degrees(self.radians)

    @property
    def radians(self):
        return atan2(self.y, self.x)

    def rotate_degrees(self, amount):
        self.rotate_radians(radians(amount))

    def rotate_radians(self, amount):
        angle = self.radians + amount
        length = self.length
        new_v = Vector2D.from_radians_and_length(angle, length)
        self.x = new_v.x
        self.y = new_v.y

    def copy(self):
        return Vector2D(self.x, self.y)
