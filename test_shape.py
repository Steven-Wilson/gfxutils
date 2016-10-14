from . import Circle
from . import Vector


def test_radius():
    c = Circle(radius=5.0)
    assert c.radius == 5.0


def test_area():
    c = Circle(radius=5.0)
    pi = 3.14159265358979323846264
    assert c.area == pi * 25.0


def test_diameter():
    c = Circle(radius=5.0)
    assert c.diameter == 10.0


def test_position():
    c = Circle(radius=1.0, position=Vector(10, 15))
    assert c.position == Vector(10, 15)


def test_within():
    c = Circle(radius=2.0, position=Vector(3, 0))
    assert c.contains(Vector(2, 1))


def test_not_within():
    c = Circle(radius=2.0, position=Vector(3, 0))
    assert not c.contains(Vector(0, 0))


def test_translate():
    c = Circle()
    c.translate(Vector(x=10, y=5))
    assert c.position == Vector(10, 5)

    c.translate(Vector(-10, 5))
    assert c.position == Vector(0, 10)


def test_scale():
    c = Circle(radius=1.0)
    c.scale(5.0)
    assert c.radius == 5.0

    c.scale(0.2)
    assert c.radius == 5.0 * 0.2


def test_bytes():
    c1 = Circle(radius=1.0, position=Vector(10, 40))
    packed_bytes = bytes(c1)
    c2 = Circle.from_bytes(packed_bytes)
    assert c1 == c2


def test_packed_size():
    b = bytes(Circle())
    assert len(b) == 8 + len(bytes(Vector()))


def test_equals():
    a = Circle(radius=3, position=Vector(2, 5.2))
    b = Circle(radius=3, position=Vector(2, 5.2))
    assert a == b
