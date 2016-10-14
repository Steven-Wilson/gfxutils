from .shape import Rect
from .vector import Vector


def test_size():
    r = Rect(Vector(0, 0), Vector(10, 20))
    assert r.width == 10
    assert r.height == 20


def test_position():
    r = Rect(Vector(10, 5), Vector(4, 3))
    assert r.x == 10
    assert r.y == 5


def test_area():
    r = Rect(Vector(10, 5), Vector(12, 30))
    assert r.area == 360


def test_perimeter():
    r = Rect(Vector(10, 5), Vector(12, 30))
    assert r.perimeter == 84


def test_within():
    r = Rect(Vector(10, 5), Vector(12, 30))
    assert r.contains(Vector(15, 15))


def test_not_within():
    r = Rect(Vector(10, 5), Vector(12, 30))
    assert not r.contains(Vector(0, 0))


def test_translate():
    r = Rect()
    r.translate(Vector(10, 5))
    assert r.position == Vector(10, 5)


def test_scale():
    r = Rect(size=Vector(20, 20))
    r.scale(5)
    assert r.area == 10000
    assert r.width == 100


def test_equals():
    a = Rect(Vector(10, 20), Vector(20, 30))
    b = Rect(Vector(10, 20), Vector(20, 30))
    assert a == b


def test_bytes():
    r1 = Rect(Vector(10, 20), Vector(20, 30))
    packed_bytes = bytes(r1)
    print(packed_bytes)
    r2 = Rect.from_bytes(packed_bytes)
    assert r1 == r2


def test_packed_size():
    b = bytes(Rect())
    assert len(b) == len(bytes(Vector())) * 2
