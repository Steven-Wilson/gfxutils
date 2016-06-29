
class Box2D:

    def __init__(self, position, size):
        if abs(size) != size:
            raise ValueError("size must be strictly positive")
        self.position = position
        self.size = size
