import pytest
from Cuerpos_celestes import CuerpoCeleste
from Clase_vector_3D import Vector3D
import math
# Constante de gravitación universal para pruebas
G_TEST = 6.674e-11

def test_cuerpo_celeste_init():
    pos = Vector3D(0, 0, 0)
    vel = Vector3D(0, 0, 0)
    cuerpo = CuerpoCeleste("Tierra", 5.972e24, pos, vel)
    assert cuerpo.id == "Tierra"
    assert cuerpo.masa == 5.972e24
    assert cuerpo.posicion.x == 0
    assert cuerpo.velocidad.y == 0

def test_cuerpo_celeste_init_invalid_mass():
    pos = Vector3D(0, 0, 0)
    vel = Vector3D(0, 0, 0)
    with pytest.raises(ValueError, match="La masa de un cuerpo celeste debe ser mayor que cero."):
        CuerpoCeleste("Tierra", 0, pos, vel)
    with pytest.raises(ValueError, match="La masa de un cuerpo celeste debe ser mayor que cero."):
        CuerpoCeleste("Tierra", -10, pos, vel)

def test_aplicar_fuerza():
    pos = Vector3D(0, 0, 0)
    vel = Vector3D(0, 0, 0)
    cuerpo = CuerpoCeleste("Test", 1.0, pos, vel) # masa = 1 para a=F
    fuerza = Vector3D(10, 0, 0)
    dt = 1.0

    cuerpo.aplicar_fuerza(fuerza, dt)
    assert cuerpo.velocidad.x == 10.0
    assert cuerpo.velocidad.y == 0.0
    assert cuerpo.velocidad.z == 0.0

    # Test con masa diferente
    cuerpo2 = CuerpoCeleste("Test2", 2.0, pos, vel)
    fuerza2 = Vector3D(10, 0, 0)
    dt2 = 1.0
    cuerpo2.aplicar_fuerza(fuerza2, dt2)
    assert cuerpo2.velocidad.x == 5.0 # a = 10/2 = 5
    assert cuerpo2.velocidad.y == 0.0

def test_mover():
    pos = Vector3D(0, 0, 0)
    vel = Vector3D(1, 2, 3)
    cuerpo = CuerpoCeleste("Test", 1.0, pos, vel)
    dt = 1.0

    cuerpo.mover(dt)
    assert cuerpo.posicion.x == 1.0
    assert cuerpo.posicion.y == 2.0
    assert cuerpo.posicion.z == 3.0

    # Test con dt diferente
    cuerpo2 = CuerpoCeleste("Test2", 1.0, Vector3D(0,0,0), Vector3D(2,0,0))
    dt2 = 0.5
    cuerpo2.mover(dt2)
    assert cuerpo2.posicion.x == 1.0

def test_energia_cinetica():
    pos = Vector3D(0, 0, 0)
    vel = Vector3D(3, 4, 0) # ||v|| = 5
    cuerpo = CuerpoCeleste("Test", 2.0, pos, vel) # masa = 2
    # K = 0.5 * m * ||v||^2 = 0.5 * 2 * (5^2) = 25
    assert cuerpo.energia_cinetica() == 25.0

    cuerpo_estatico = CuerpoCeleste("Static", 1.0, pos, Vector3D(0,0,0))
    assert cuerpo_estatico.energia_cinetica() == 0.0

def test_energia_potencial_con():
    cuerpo1 = CuerpoCeleste("C1", 100.0, Vector3D(0, 0, 0), Vector3D(0, 0, 0))
    cuerpo2 = CuerpoCeleste("C2", 50.0, Vector3D(3, 0, 0), Vector3D(0, 0, 0)) # Distancia = 3

    # U = -G * (m1 * m2) / r = -G_TEST * (100 * 50) / 3 = -G_TEST * 5000 / 3
    expected_potential = -G_TEST * (100.0 * 50.0) / 3.0
    assert abs(cuerpo1.energia_potencial_con(cuerpo2, G_TEST) - expected_potential) < 1e-9

    cuerpo3 = CuerpoCeleste("C3", 10.0, Vector3D(0, 4, 0), Vector3D(0, 0, 0)) # Distancia con C1 = 4
    expected_potential_c1_c3 = -G_TEST * (100.0 * 10.0) / 4.0
    assert abs(cuerpo1.energia_potencial_con(cuerpo3, G_TEST) - expected_potential_c1_c3) < 1e-9

def test_energia_potencial_con_same_position():
    cuerpo1 = CuerpoCeleste("C1", 100.0, Vector3D(0, 0, 0), Vector3D(0, 0, 0))
    cuerpo_same_pos = CuerpoCeleste("C_same", 50.0, Vector3D(0, 0, 0), Vector3D(0, 0, 0))
    assert cuerpo1.energia_potencial_con(cuerpo_same_pos, G_TEST) == float('-inf')

def test_cuerpo_to_from_dict():
    pos = Vector3D(1.0, 2.0, 3.0)
    vel = Vector3D(0.1, 0.2, 0.3)
    cuerpo = CuerpoCeleste("Marte", 6.39e23, pos, vel)

    data = cuerpo.to_dict()
    assert data["id"] == "Marte"
    assert data["masa"] == 6.39e23
    assert data["posicion"] == [1.0, 2.0, 3.0]
    assert data["velocidad"] == [0.1, 0.2, 0.3]

    loaded_cuerpo = CuerpoCeleste.from_dict(data)
    assert loaded_cuerpo.id == "Marte"
    assert loaded_cuerpo.masa == 6.39e23
    assert loaded_cuerpo.posicion.x == 1.0
    assert loaded_cuerpo.posicion.y == 2.0
    assert loaded_cuerpo.posicion.z == 3.0
    assert loaded_cuerpo.velocidad.x == 0.1
    assert loaded_cuerpo.velocidad.y == 0.2
    assert loaded_cuerpo.velocidad.z == 0.3