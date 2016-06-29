from math import isclose
from simplevector.box import Box2D
from simplevector.vector import Vector2D

pi = 3.14159265358979323846264


def close_enough(a, b):
    return isclose(a, b, rel_tol=0.0001, abs_tol=0.00001)


def test_area():
    box = Box2D(Vector2D(1, 1), Vector2D(50, 50))
    assert box.area == 2500


def test_size():
    box = Box2D(Vector2D(0, 0), Vector2D(100, 100))
    assert close_enough(box.bottom_left.y, 0)
    assert close_enough(box.top_left.y, 100)
    assert close_enough(box.bottom_left.x, 0)
    assert close_enough(box.bottom_right.x, 100)
    assert box.center == Vector2D(50, 50)


def test_rotation():
    box = Box2D(Vector2D(0, 0), Vector2D(100, 100),
                origin=Vector2D(50, 50),
                rotation=pi / 2)
    assert close_enough(box.top_left.x, -50)
    assert close_enough(box.top_left.y, -50)
    assert close_enough(box.bottom_left.x, 50)
    assert close_enough(box.bottom_left.y, -50)
    assert close_enough(box.bottom_right.x, 50)
    assert close_enough(box.bottom_right.y, 50)
    assert close_enough(box.top_right.x, -50)
    assert close_enough(box.top_right.y, 50)
    assert box.center == Vector2D(0, 0)


def test_origin():
    box = Box2D(Vector2D(0, 0), Vector2D(100, 100),
                origin=Vector2D(50, 50))
    assert close_enough(box.bottom_left.y, -50)
    assert close_enough(box.top_left.y, 50)
    assert close_enough(box.bottom_left.x, -50)
    assert close_enough(box.bottom_right.x, 50)
    assert box.center == Vector2D(0, 0)


def test_position():
    box = Box2D(Vector2D(-50, -50), Vector2D(100, 100))
    assert close_enough(box.bottom_left.y, -50)
    assert close_enough(box.top_left.y, 50)
    assert close_enough(box.bottom_left.x, -50)
    assert close_enough(box.bottom_right.x, 50)
    assert box.center == Vector2D(0, 0)
