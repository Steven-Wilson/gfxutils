from random import random
from simplevector import Vector2D, epsilon


def generate_vectors(number_of_vectors, iterations=100):
    if number_of_vectors == 1:
        for _ in range(iterations):
            yield Vector2D(random(), random())
    else:
        for _ in range(iterations):
            result = []
            for _ in range(number_of_vectors):
                result.append(Vector2D(random(), random()))
            yield tuple(result)


def test_concat_length_should_be_less_than_path():
    for v1, v2 in generate_vectors(2):
        v3 = v1 + v2
        assert (v1.length + v2.length) - v3.length >= 0


def test_vector_subtracted_from_itself_should_be_0():
    for v1 in generate_vectors(1):
        v2 = v1 - v1
        assert abs(v2.length) < epsilon


def test_vector_rotated_180_and_negated_should_be_same():
    for v1 in generate_vectors(1):
        v2 = v1.copy()
        v2.rotate_degrees(180)
        v3 = v1 + v2
        assert abs(v3.length) < epsilon


def test_vector_divide_by_2_should_half_length():
    for v1 in generate_vectors(1):
        v2 = v1 / 2
        v3 = v1.copy()
        assert v1 == v3
        v3 /= 2
        assert v2 == v3
        assert abs((v1.length / 2) - v3.length) < epsilon


def test_vector_mul_then_div_should_match():
    for v1 in generate_vectors(1):
        v2 = v1 * 3.238 / 3.238
        assert v1 == v2


def test_normalize():
    for v1 in generate_vectors(1):
        v2 = v1.copy()
        v2.normalize()
        v3 = v1.normalized
        assert v2 == v3
        assert v1 != v2
        assert v1 != v3
        assert abs(v1.radians - v2.radians) < epsilon
        assert abs(v1.radians - v3.radians) < epsilon
        assert abs(v1.degrees - v2.degrees) < epsilon
        assert abs(v1.degrees - v3.degrees) < epsilon
