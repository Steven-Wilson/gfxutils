from .shape import Line
from .vector import V2


def test_length():
    l1 = Line(V2(0, 0), V2(10, 0))
    l1.length == 10

    l2 = Line(V2(5, 10), V2(5, 10))
    l2.length == 0


def test_intersect():
    l1 = Line(V2(0, 0), V2(10, 10))
    l2 = Line(V2(0, 10), V2(10, 0))
    assert l1.intersection(l2) == V2(5, 5)


def test_parallel():
    l1 = Line(V2(0, 0), V2(10, 10))
    l2 = Line(V2(5, 5), V2(15, 15))


# def test_vertical_line():
#     l1 = Line(V2(1, 0), V2(1, 10))
#     l2 = Line(V2(11, 0), V2(10, 10))
#     assert l1.intersection(l2) == V2(1, 1)
