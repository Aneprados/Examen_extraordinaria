from Clase_vector_3D import Vector3D
import math

class CuerpoCeleste:
    def __init__(self, id: str, masa: float, posicion: Vector3D, velocidad: Vector3D):
        if masa <= 0:
            raise ValueError("La masa de un cuerpo celeste debe ser mayor que cero.")
        self.id = id
        self.masa = masa
        self.posicion = posicion
        self.velocidad = velocidad

    def aplicar_fuerza(self, fuerza: Vector3D, dt: float):
        # a = F/m
        aceleracion = fuerza * (1.0 / self.masa)
        # v(t+dt) = v(t) + a * dt
        self.velocidad = self.velocidad + aceleracion * dt

    def mover(self, dt: float):
        # r(t+dt) = r(t) + v(t) * dt
        self.posicion = self.posicion + self.velocidad * dt

    def energia_cinetica(self) -> float:
        # K = 0.5 * m * ||v||^2
        return 0.5 * self.masa * (self.velocidad.magnitude()**2)

    def energia_potencial_con(self, otro: 'CuerpoCeleste', G: float) -> float:
        # U = -G * (m1 * m2) / ||r1 - r2||
        distancia_vector = self.posicion - otro.posicion
        distancia = distancia_vector.magnitude()
        if distancia == 0:
            return float('-inf') # Cuerpos en la misma posición, potencial infinito
        return -G * (self.masa * otro.masa) / distancia

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "masa": self.masa,
            "posicion": self.posicion.to_list(),
            "velocidad": self.velocidad.to_list()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'CuerpoCeleste':
        posicion = Vector3D.from_list(data["posicion"])
        velocidad = Vector3D.from_list(data["velocidad"])
        return cls(data["id"], data["masa"], posicion, velocidad)