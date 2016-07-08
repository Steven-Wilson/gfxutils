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
        - Addition and Subtraction is vector addition and subtraction
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
        - Multiplication and Division is scalar addition and subtraction
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
- Shapes
    - Circle
