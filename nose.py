import math

class Vector3D:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        if not isinstance(other, Vector3D):
            raise TypeError("El operando debe ser de tipo Vector3D")
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        if not isinstance(other, Vector3D):
            raise TypeError("El operando debe ser de tipo Vector3D")
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float):
        if not isinstance(scalar, (int, float)):
            raise TypeError("El escalar debe ser un número")
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def __repr__(self):
        return f"Vector3D(x={self.x}, y={self.y}, z={self.z})"

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"