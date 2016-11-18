import pytest
from .vector import V3
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
    return V3(rng(-20, 20),
              rng(-20, 20),
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
    assert close_enough(v1.x_radians - v2.x_radians, 0)
    assert close_enough(v1.x_radians - v3.x_radians, 0)
    assert close_enough(v1.x_degrees - v2.x_degrees, 0)
    assert close_enough(v1.x_degrees - v3.x_degrees, 0)
    assert close_enough(v1.y_radians - v2.y_radians, 0)
    assert close_enough(v1.y_radians - v3.y_radians, 0)
    assert close_enough(v1.y_degrees - v2.y_degrees, 0)
    assert close_enough(v1.y_degrees - v3.y_degrees, 0)
    assert close_enough(v1.z_radians - v2.z_radians, 0)
    assert close_enough(v1.z_radians - v3.z_radians, 0)
    assert close_enough(v1.z_degrees - v2.z_degrees, 0)
    assert close_enough(v1.z_degrees - v3.z_degrees, 0)
    v4 = v1.copy
    v4.normalized = V3(1, 0, 0)
    assert close_enough(v4.length, v1.length)
    assert close_enough(v4.x_degrees, 0)
    assert close_enough(v4.y_degrees, 90)
    assert close_enough(v4.z_degrees, 0)


def test_representation():
    v = V3(3.5, 2.125, -1.2)
    assert repr(v) == 'V3(3.500, 2.125, -1.200)'


def test_bytes(v1):
    # pack v.x and v.y into bytes object b
    packed_bytes = bytes(v1)

    # Make a new vector from the bytes object
    v2 = V3.from_bytes(packed_bytes)

    # The new object should be the same
    assert v1 == v2


def test_copy(v1):
    v2 = v1.copy
    assert v1 == v2


def test_index_access(v1, v2):
    assert close_enough(v1.x - v1[0], 0)
    assert close_enough(v1.y - v1[1], 0)
    assert close_enough(v1.z - v1[2], 0)

    v1[0] = v2.x
    v1[1] = v2.y
    v1[2] = v2.z

    assert v1 == v2

    with pytest.raises(IndexError):
        v1.x = v1[3]

    with pytest.raises(IndexError):
        v1[3] = 5

    with pytest.raises(NotImplementedError):
        del v1[0]


def test_add(v1, v2):
    v3 = v1 + v2
    v4 = v1.copy
    v4 += v2
    assert v3 == v4
    assert close_enough(v3.x, v1.x + v2.x)
    assert close_enough(v3.y, v1.y + v2.y)
    assert close_enough(v3.z, v1.z + v2.z)


def test_sub(v1, v2):
    v3 = v1 - v2
    v4 = v1.copy
    v4 -= v2
    assert v3 == v4
    assert close_enough(v3.x, v1.x - v2.x)
    assert close_enough(v3.y, v1.y - v2.y)
    assert close_enough(v3.z, v1.z - v2.z)


def test_mul(v1):
    f = rng(-20, 20)
    v2 = v1 * f
    v3 = v1.copy
    v3 *= f
    assert v2 == v3
    assert close_enough(v2.x, v1.x * f)
    assert close_enough(v2.y, v1.y * f)
    assert close_enough(v2.z, v1.z * f)


def test_div(v1):
    f = rng(-20, 20)
    v2 = v1 / f
    v3 = v1.copy
    v3 /= f
    assert v2 == v3
    assert close_enough(v2.x, v1.x / f)
    assert close_enough(v2.y, v1.y / f)
    assert close_enough(v2.z, v1.z / f)


def test_not_equal():
    a = V3(1, 2, 3)
    assert a != V3(2, 2, 3)
    assert a != V3(1, 3, 3)
    assert a != V3(1, 2, 2)
    assert a == V3(1, 2, 3)


def test_neg(v1):
    v2 = -v1
    assert close_enough(v2.length, v1.length)
    assert close_enough(v1.x, -v2.x)
    assert close_enough(v1.y, -v2.y)


def test_pos(v1):
    v2 = +v1
    assert v1 == v2


def test_abs(v1):
    assert abs(v1) == v1.length


def test_hash(v1):
    assert hash(v1) == hash(v1)


def test_bool(v1):
    assert v1


def test_sequence_forward(v1):
    forward = [v1.x, v1.y, v1.z]
    for a, b in zip(forward, v1):
        assert close_enough(a, b)


def test_sequence_backward(v1):
    backward = [v1.z, v1.y, v1.x]
    for a, b in zip(backward, reversed(v1)):
        assert close_enough(a, b)


def test_contains(v1):
    assert v1.x in v1
    assert v1.y in v1
    assert v1.z in v1


def test_not_contains(v1):
    v1.x = 0
    v1.y = 2
    assert 1 not in v1


def test_length(v1):
    assert close_enough(v1.length_squared,
                        v1.length * v1.length)
    v1.length = 10
    v1.normalized = V3(1, 0, 0)
    assert close_enough(v1.x, 10)
    assert close_enough(v1.y, 0)
    assert close_enough(v1.length_squared, 100)


def test_dot(v1):
    assert close_enough(v1.dot_product(v1), v1.length_squared)


def test_packed_size():
    b = bytes(V3())
    assert len(b) == 24


def test_write(v1):
    writer = MockWriter()
    v1.write(writer)
    assert writer.written == bytes(v1)
