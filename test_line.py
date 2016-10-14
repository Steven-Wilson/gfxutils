from .shape import Line
from .vector import Vector


def test_length():
    l1 = Line(Vector(0, 0), Vector(10, 0))
    l1.length == 10

    l2 = Line(Vector(5, 10), Vector(5, 10))
    l2.length == 0


def test_intersect():
    l1 = Line(Vector(0, 0), Vector(10, 10))
    l2 = Line(Vector(0, 10), Vector(10, 0))
    assert l1.intersection(l2) == Vector(5, 5)


def test_parallel():
    l1 = Line(Vector(0, 0), Vector(10, 10))
    l2 = Line(Vector(5, 5), Vector(15, 15))


# def test_vertical_line():
#     l1 = Line(Vector(1, 0), Vector(1, 10))
#     l2 = Line(Vector(11, 0), Vector(10, 10))
#     assert l1.intersection(l2) == Vector(1, 1)
