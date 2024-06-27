import math


class Vector2:
    """
    A Vector2 class for Python.

    Useful for 2D directions, positions and has many built-in functions to help with math.
    """

    x = 0.0
    y = 0.0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Vector2 ({self.x}, {self.y})"

    def __add__(self, other):
        """
        Overloads the + operator for vector addition.
        """
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        else:
            return Vector2(self.x + other, self.y + other)

    def __sub__(self, other):
        """
        Overloads the "-" operator for vector subtraction.
        """
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        else:
            return Vector2(self.x - other, self.y - other)

    def __mul__(self, other):
        """
        Overloads the "*" operator for vector multiplication (scalar or component-wise).
        """
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        else:
            return Vector2(self.x * other, self.y * other)

    def __truediv__(self, other):
        """
        Overloads the "/" operator for vector division (scalar division).
        """
        if isinstance(other, (int, float)):
            if other != 0:
                return Vector2(self.x / other, self.y / other)
            else:
                return Vector2(0, 0)
        else:
            if other.x == 0:
                other.x = 1
            if other.y == 0:
                other.y = 1
            return Vector2(self.x / other.x, self.y / other.y)

    def dot(self, other):
        """
        Returns the dot product of the two vectors
        """
        if not isinstance(other, Vector2):
            raise TypeError("Dot product can only be calculated between two Vector2 objects")
        return self.x * other.x + self.y * other.y

    def magnitude(self):
        """
        Returns the length of the vector

        :return: float
        """

        return math.sqrt((self.x * self.x) + (self.y * self.y))

    def sqr_magnitude(self):
        """
        Returns the squared length of the vector.
        Consider using this if possible, as the sqrt() operation isn't fast (compared to "+", "-" and "*")

        :return: float
        """

        return (self.x * self.x) + (self.y * self.y)

    def normalized(self):
        """
        Returns a normalized vector

        :return: Vector3
        """

        mag = self.magnitude()
        return Vector2(self.x/mag, self.y/mag)

    def shorten(self, amount):
        mag = self.sqr_magnitude()
        scale = (mag - amount * amount) / mag

        return self * scale
