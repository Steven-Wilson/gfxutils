# gfxutils
A group of simple implementations for common utilities used in graphical applications:
- Vectors (2D)
    - Importing
    ```python
        from gfxutils.vector import Vector

        pi = 3.14159265358979323846264

        v1 = Vector(x=10, y=10)
        assert v1.length == 14.14213562373095048

        v2 = Vector.from_degrees_and_length(45, 14.14213562373095048)
        assert v1 == v2
        assert abs(v2.x - 10) < 0.0001
        assert abs(v2.y - 10) < 0.0001

        v3 = Vector.from_radians_and_length(pi / 4, 14.14213562373095048)
        assert v1 == v3

    ```
    - Vector Math
        - Addition and Subtraction is element-wise vector math
        ```python

            v1 = Vector(x=10, y=20)
            v2 = Vector(y=1)
            v3 = v1 + v2
            assert v3 == Vector(10, 21)
            v4 = v3 - Vector(x=5)
            assert v4 == Vector(5, 21)
            v1 += v2
            assert v1 == v3
            v3 -= Vector(x=5)
            assert v4 == v3
        ```
        - Multiplication and Division is Vector * Scalar and Vector / Scalar
        ```python
            v1 = Vector(x=10, y=20)
            v2 = v1 * 2
            assert v2 == Vector(20, 40)
            v3 = v1 / 2
            assert v3 == Vector(5, 10)
            v4 = v1.copy
            v4 *= 2
            assert v4 == Vector(20, 40)
            v5 = v1.copy
            v5 /= 2
            assert v5 == Vector(5, 10)
        ```
    - Angles are measured counterclockwise from the positive x axis
    ```python
        v1 = Vector(x=10, y=10)
        # within rounding of 45°
        assert abs(v1.degrees - 45) < 0.0001
        assert abs(v1.radians - pi / 4) < 0.0001

        v1.degrees += 45
        assert v1 == Vector(y=v1.length)
    ```
    - Normalization (equivalent to setting the length to 1)
    ```python
        v1 = Vector(x=10, y=10)
        assert v1.length == 14.14213562373095048

        # create a normalized copy without modifying v1
        v2 = v1.normalized
        assert v1.length == 14.14213562373095048
        assert abs(v2.length - 1) < 0.0001

        # normalize v1 in-place
        v1.normalize()
        assert abs(v1.length - 1) < 0.0001
    ```
- Colors
    - __Use a proper c-based library to manipulate bitmaps__
        - A list of Color instances long enough to process a 1920x1080 bitmap (2,073,600 instances) will take several seconds to make
        - SDL2, pyglet, pillow, and numpy may be acceptable choices depending on your need
    - Creation of Color instances
    ```python
        white = Color(red=1.0, green=1.0, blue=1.0)
        assert white.hex == '#FFFFFFFF'

        clear = Color(alpha=0.0)
        assert clear.hex == '#00000000'

        red = Color.from_hsb(hue=0.0, saturation=1.0, brightness=1.0)
        assert red.hex == '#FF0000FF'
    ```
    - Primary Colors
    ```python
        red = Color(red=1.0)
        assert red.hex == '#FF0000FF'

        green = Color(green=1.0)
        assert green.hex == '#00FF00FF'

        blue = Color(blue=1.0)
        assert blue.hex == '#0000FFFF'
    ```
    - Transparency via an alpha channel
    ```python
        transparent_black = Color(alpha=0.5)
        assert transparent_black.hex == '#0000007F'
    ```
    - Comparisons use equality
    ```python
        red1 = Color(red=1.0)
        red2 = Color.from_hsb(hue=0.0, saturation=1.0, brightness=1.0)
        assert red1 == red2
    ```
    - Bytes built-in is supported
    ```python
        green = Color(green=1.0, alpha=0.5)
        assert bytes(green) == b'\x00\xFF\x00\x7F'
    ```
- Shapes
    - Circle
        - Documentation Coming Soon
    - TODO:
        - Line
        - Triangle
        - Rectangle
