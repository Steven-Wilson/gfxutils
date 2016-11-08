from .shape import Rect
from .vector import V2


class MockWriter:

    def __init__(self):
        self.written = None

    def write(self, value):
        self.written = value


def test_size():
    r = Rect(V2(0, 0), V2(10, 20))
    assert r.width == 10
    assert r.height == 20


def test_position():
    r = Rect(V2(10, 5), V2(4, 3))
    assert r.x == 10
    assert r.y == 5


def test_area():
    r = Rect(V2(10, 5), V2(12, 30))
    assert r.area == 360


def test_perimeter():
    r = Rect(V2(10, 5), V2(12, 30))
    assert r.perimeter == 84


def test_within():
    r = Rect(V2(10, 5), V2(12, 30))
    assert r.contains(V2(15, 15))


def test_not_within():
    r = Rect(V2(10, 5), V2(12, 30))
    assert not r.contains(V2(0, 0))


def test_translate():
    r = Rect()
    r.translate(V2(10, 5))
    assert r.position == V2(10, 5)


def test_scale():
    r = Rect(size=V2(20, 20))
    r.scale(5)
    assert r.area == 10000
    assert r.width == 100


def test_equals():
    a = Rect(V2(10, 20), V2(20, 30))
    b = Rect(V2(10, 20), V2(20, 30))
    assert a == b


def test_bytes():
    r1 = Rect(V2(10, 20), V2(20, 30))
    packed_bytes = bytes(r1)
    print(packed_bytes)
    r2 = Rect.from_bytes(packed_bytes)
    assert r1 == r2


def test_packed_size():
    b = bytes(Rect())
    assert len(b) == len(bytes(V2())) * 2


def test_not_equal():
    a = Rect(position=V2(10, 20), size=V2(30, 40))
    b = Rect(position=V2(10, 15), size=V2(30, 40))
    c = Rect(position=V2(10, 20), size=V2(20, 40))
    assert b != a
    assert c != a


def test_write():
    a = Rect(position=V2(10, 20), size=V2(30, 40))
    writer = MockWriter()
    a.write(writer)
    assert writer.written == bytes(a)


def test_x_position():
    a = Rect(position=V2(10, 20), size=V2(30, 40))
    assert a.x1 == 10


def test_y_position():
    a = Rect(position=V2(10, 20), size=V2(30, 40))
    assert a.y1 == 20
