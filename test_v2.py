import pytest
from . import V2
from random import random


pi = 3.14159265358979323846264


class MockWriter:

    def __init__(self):
        self.written = None

    def write(self, value):
        self.written = value


def rng(a, b):
    return random() * (b - a) - (b - a) / 2


def close_enough(a, b):
    return abs(a - b) < 0.0001


def random_vector():
    return V2(rng(-20, 20),
              rng(-20, 20))


@pytest.fixture
def v1():
    return random_vector()


@pytest.fixture
def v2():
    return random_vector()


def test_concat_length_should_be_less_than_path(v1, v2):
    v3 = v1 + v2
    assert (v1.length + v2.length) - v3.length >= 0


def test_vector_subtracted_from_itself_should_be_0(v1):
    v2 = v1 - v1
    assert close_enough(v2.length, 0)


def test_vector_rotated_180_and_negated_should_be_same(v1):
    v2 = v1.copy
    v2.degrees += 180
    v3 = v1 + v2
    assert close_enough(v3.length, 0)

    v4 = v1.copy
    v4.radians += pi
    v5 = v1 + v4
    assert close_enough(v5.length, 0)


def test_vector_divide_by_2_should_half_length(v1):
    v2 = v1 / 2
    v3 = v1.copy
    assert v1 == v3
    v3 /= 2
    assert v2 == v3
    assert close_enough((v1.length / 2) - v3.length, 0)


def test_vector_mul_then_div_should_match(v1):
    v2 = v1 * 3.238 / 3.238
    assert v1 == v2


def test_normalize(v1):
    v2 = v1.copy
    v2.normalize()
    v3 = v1.normalized
    assert v2 == v3
    assert v1 != v2
    assert v1 != v3
    assert close_enough(v1.radians - v2.radians, 0)
    assert close_enough(v1.radians - v3.radians, 0)
    assert close_enough(v1.degrees - v2.degrees, 0)
    assert close_enough(v1.degrees - v3.degrees, 0)
    v4 = v1.copy
    v4.normalized = V2(1, 0)
    assert close_enough(v4.length, v1.length)
    assert close_enough(v4.degrees, 0)


def test_alternate_constructors(v1):
    v2 = V2.from_radians_and_length(v1.radians, v1.length)
    v3 = V2.from_degrees_and_length(v1.degrees, v1.length)
    assert v1 == v2
    assert v1 == v3


def test_representation():
    v = V2(3.5, 2.125)
    assert repr(v) == "V2(3.500, 2.125)"


def test_bytes(v1):
    # pack v.x and v.y into bytes object b
    packed_bytes = bytes(v1)

    # Make a new vector from the bytes object
    v2 = V2.from_bytes(packed_bytes)

    # The new object should be the same
    assert v1 == v2


def test_copy(v1):
    v2 = v1.copy
    assert v1 == v2


def test_index_access(v1, v2):
    assert close_enough(v1.x - v1[0], 0)
    assert close_enough(v1.y - v1[1], 0)

    v1[0] = v2.x
    v1[1] = v2.y

    assert v1 == v2

    with pytest.raises(IndexError):
        v1.x = v1[2]

    with pytest.raises(IndexError):
        v1[2] = 5

    with pytest.raises(NotImplementedError):
        del v1[0]


def test_add(v1, v2):
    v3 = v1 + v2
    v4 = v1.copy
    v4 += v2
    assert v3 == v4
    assert close_enough(v3.x, v1.x + v2.x)
    assert close_enough(v3.y, v1.y + v2.y)


def test_sub(v1, v2):
    v3 = v1 - v2
    v4 = v1.copy
    v4 -= v2
    assert v3 == v4
    assert close_enough(v3.x, v1.x - v2.x)
    assert close_enough(v3.y, v1.y - v2.y)


def test_mul(v1):
    f = rng(-20, 20)
    v2 = v1 * f
    v3 = v1.copy
    v3 *= f
    assert v2 == v3
    assert close_enough(v2.x, v1.x * f)
    assert close_enough(v2.y, v1.y * f)


def test_div(v1):
    f = rng(-20, 20)
    v2 = v1 / f
    v3 = v1.copy
    v3 /= f
    assert v2 == v3
    assert close_enough(v2.x, v1.x / f)
    assert close_enough(v2.y, v1.y / f)


def test_neg(v1):
    v2 = -v1
    assert close_enough(v2.length, v1.length)
    assert close_enough(v1.x, -v2.x)
    assert close_enough(v1.y, -v2.y)


def test_pos(v1):
    v2 = +v1
    assert v1 == v2


def test_abs(v1):
    v2 = abs(v1)
    assert close_enough(abs(v1.x), v2.x)
    assert close_enough(abs(v1.y), v2.y)


def test_hash(v1):
    assert hash(v1) == hash(v1)


def test_bool(v1):
    assert v1


def test_sequence_forward(v1):
    forward = [v1.x, v1.y]
    for a, b in zip(forward, v1):
        assert close_enough(a, b)


def test_sequence_backward(v1):
    backward = [v1.y, v1.x]
    for a, b in zip(backward, reversed(v1)):
        assert close_enough(a, b)


def test_contains(v1):
    assert v1.x in v1
    assert v1.y in v1


def test_not_contains(v1):
    v1.x = 0
    v1.y = 2
    assert 1 not in v1


def test_length(v1):
    assert close_enough(v1.length_squared,
                        v1.length * v1.length)
    v1.length = 10
    v1.radians = 0
    assert close_enough(v1.x, 10)
    assert close_enough(v1.y, 0)
    assert close_enough(v1.length_squared, 100)


def test_dot(v1):
    assert close_enough(v1.dot_product(v1), v1.length_squared)


def test_packed_size():
    b = bytes(V2())
    assert len(b) == 16


def test_documentation():
    v1 = V2(x=10, y=10)
    assert v1.length == 14.14213562373095048

    v2 = V2.from_degrees_and_length(45, 14.14213562373095048)
    assert v1 == v2
    assert abs(v2.x - 10) < 0.0001
    assert abs(v2.y - 10) < 0.0001

    v3 = V2.from_radians_and_length(pi / 4, 14.14213562373095048)
    assert v1 == v3


def test_documentation_add_sub():
    v1 = V2(x=10, y=20)
    v2 = V2(y=1)
    v3 = v1 + v2
    assert v3 == V2(10, 21)
    v4 = v3 - V2(x=5)
    assert v4 == V2(5, 21)
    v1 += v2
    assert v1 == v3
    v3 -= V2(x=5)
    assert v4 == v3


def test_documentation_mul_div():
    v1 = V2(x=10, y=20)
    v2 = v1 * 2
    assert v2 == V2(20, 40)
    v3 = v1 / 2
    assert v3 == V2(5, 10)
    v4 = v1.copy
    v4 *= 2
    assert v4 == V2(20, 40)
    v5 = v1.copy
    v5 /= 2
    assert v5 == V2(5, 10)


def test_documentation_angles():
    v1 = V2(x=10, y=10)
    # within rounding of 45°
    assert abs(v1.degrees - 45) < 0.0001
    assert abs(v1.radians - pi / 4) < 0.0001

    v1.degrees += 45
    assert v1 == V2(y=v1.length)


def test_documentation_normalization():
    v1 = V2(x=10, y=10)
    assert v1.length == 14.14213562373095048

    # create a normalized copy without modifying v1
    v2 = v1.normalized
    assert v1.length == 14.14213562373095048
    assert abs(v2.length - 1) < 0.0001

    # normalize v1 in-place
    v1.normalize()
    assert abs(v1.length - 1) < 0.0001


def test_not_equal():
    a = V2(1, 2)
    assert a != V2(2, 2)
    assert a != V2(1, 3)
    assert a == V2(1, 2)


def test_x_vector():
    a = V2(10, 20)
    assert a.x_vector == V2(10, 0)
    assert a == V2(10, 20)


def test_y_vector():
    a = V2(10, 20)
    assert a.y_vector == V2(0, 20)
    assert a == V2(10, 20)


def test_mirror(v1):
    a = v1.mirror
    assert v1.x == -a.x
    assert v1.y == -a.y
    assert a == -v1


def test_mirror_x(v1):
    a = v1.mirror_x
    assert v1.x == a.x
    assert v1.y == -a.y


def test_mirror_y(v1):
    a = v1.mirror_y
    assert v1.x == -a.x
    assert v1.y == a.y


def test_write(v1):
    writer = MockWriter()
    v1.write(writer)
    assert writer.written == bytes(v1)
