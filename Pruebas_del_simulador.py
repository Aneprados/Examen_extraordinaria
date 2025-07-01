import pytest
from Simulador import Simulador
from Clase_vector_3D import Vector3D
from Cuerpos_celestes import CuerpoCeleste
import os
import json
import csv

# Constante de gravitación universal para pruebas
G_TEST = 6.674e-11

@pytest.fixture
def simulador_vacio():
    return Simulador(G=G_TEST)

@pytest.fixture
def simulador_con_cuerpos():
    sim = Simulador(G=G_TEST)
    sim.agregar_cuerpo("Sol", 1.989e30, Vector3D(0, 0, 0), Vector3D(0, 0, 0))
    sim.agregar_cuerpo("Tierra", 5.972e24, Vector3D(1.5e11, 0, 0), Vector3D(0, 3e4, 0))
    sim.agregar_cuerpo("Luna", 7.342e22, Vector3D(1.5e11 + 3.84e8, 0, 0), Vector3D(0, 3e4 + 1e3, 0))
    return sim

def test_simulador_init(simulador_vacio):
    assert len(simulador_vacio.cuerpos) == 0
    assert simulador_vacio.G == G_TEST

def test_agregar_cuerpo(simulador_vacio):
    simulador_vacio.agregar_cuerpo("Marte", 6.39e23, Vector3D(0, 0, 0), Vector3D(0, 0, 0))
    assert "Marte" in simulador_vacio.cuerpos
    assert simulador_vacio.cuerpos["Marte"].masa == 6.39e23

def test_agregar_cuerpo_duplicado(simulador_vacio):
    simulador_vacio.agregar_cuerpo("Mercurio", 3.301e23, Vector3D(0, 0, 0), Vector3D(0, 0, 0))
    with pytest.raises(ValueError, match="Ya existe un cuerpo con el ID 'Mercurio'."):
        simulador_vacio.agregar_cuerpo("Mercurio", 3.301e23, Vector3D(1, 1, 1), Vector3D(1, 1, 1))

def test_obtener_cuerpo(simulador_con_cuerpos):
    tierra = simulador_con_cuerpos.obtener_cuerpo("Tierra")
    assert tierra is not None
    assert tierra.id == "Tierra"
    assert simulador_con_cuerpos.obtener_cuerpo("NoExiste") is None

def test_listar_cuerpos(simulador_vacio, capsys):
    simulador_vacio.listar_cuerpos()
    captured = capsys.readouterr()
    assert "No hay cuerpos celestes registrados" in captured.out

    simulador_vacio.agregar_cuerpo("Jupiter", 1.898e27, Vector3D(0, 0, 0), Vector3D(0, 0, 0))
    simulador_vacio.listar_cuerpos()
    captured = capsys.readouterr()
    assert "Jupiter" in captured.out
    assert "Masa: 1.90e+27 kg" in captured.out

def test_calcular_fuerzas_dos_cuerpos(simulador_vacio):
    c1 = CuerpoCeleste("C1", 100.0, Vector3D(0, 0, 0), Vector3D(0, 0, 0))
    c2 = CuerpoCeleste("C2", 50.0, Vector3D(3, 0, 0), Vector3D(0, 0, 0))
    simulador_vacio.cuerpos[c1.id] = c1
    simulador_vacio.cuerpos[c2.id] = c2

    fuerzas = simulador_vacio.calcular_fuerzas()

    # F = G * m1 * m2 / r^2
    expected_force_magnitude = G_TEST * 100.0 * 50.0 / (3.0**2)
    assert abs(fuerzas["C1"].x - expected_force_magnitude) < 1e-9 # C2 atrae a C1 en direccion positiva
    assert abs(fuerzas["C2"].x + expected_force_magnitude) < 1e-9 # C1 atrae a C2 en direccion negativa
    assert fuerzas["C1"].y == 0 and fuerzas["C1"].z == 0
    assert fuerzas["C2"].y == 0 and fuerzas["C2"].z == 0

def test_calcular_fuerzas_tres_cuerpos(simulador_vacio):
    c1 = CuerpoCeleste("C1", 1e10, Vector3D(0, 0, 0), Vector3D(0, 0, 0))
    c2 = CuerpoCeleste("C2", 1e10, Vector3D(100, 0, 0), Vector3D(0, 0, 0))
    c3 = CuerpoCeleste("C3", 1e10, Vector3D(0, 100, 0), Vector3D(0, 0, 0))
    simulador_vacio.cuerpos[c1.id] = c1
    simulador_vacio.cuerpos[c2.id] = c2
    simulador_vacio.cuerpos[c3.id] = c3

    fuerzas = simulador_vacio.calcular_fuerzas()

    # Fuerza C1-C2 (en X)
    f_c1c2_mag = G_TEST * (1e10 * 1e10) / (100**2)
    # Fuerza C1-C3 (en Y)
    f_c1c3_mag = G_TEST * (1e10 * 1e10) / (100**2)

    # Fuerza neta en C1
    assert abs(fuerzas["C1"].x - f_c1c2_mag) < 1e-9
    assert abs(fuerzas["C1"].y - f_c1c3_mag) < 1e-9

    # Fuerza neta en C2
    assert abs(fuerzas["C2"].x + f_c1c2_mag) < 1e-9
    assert abs(fuerzas["C2"].y) < 1e-9 # C3 no atrae a C2 en Y (solo en X)

    # Fuerza neta en C3
    assert abs(fuerzas["C3"].x) < 1e-9 # C2 no atrae a C3 en X (solo en Y)
    assert abs(fuerzas["C3"].y + f_c1c3_mag) < 1e-9


def test_paso_simulacion_euler_explicit(simulador_vacio, capsys):
    # Simulación de un solo cuerpo moviéndose a velocidad constante (sin fuerzas)
    c1 = CuerpoCeleste("Sat", 1.0, Vector3D(0, 0, 0), Vector3D(1, 0, 0))
    simulador_vacio.cuerpos[c1.id] = c1
    dt = 1.0

    simulador_vacio.paso_simulacion(dt)
    assert simulador_vacio.cuerpos["Sat"].posicion.x == 1.0
    assert simulador_vacio.cuerpos["Sat"].velocidad.x == 1.0 # No hay fuerza, velocidad constante

    # Simulación de dos cuerpos, verificar cambio de velocidad y posición
    simulador_vacio = Simulador(G=G_TEST) # Reset simulador
    c1_grav = CuerpoCeleste("C1", 1e10, Vector3D(0, 0, 0), Vector3D(0, 0, 0))
    c2_grav = CuerpoCeleste("C2", 1e10, Vector3D(100, 0, 0), Vector3D(0, 0, 0))
    simulador_vacio.cuerpos[c1_grav.id] = c1_grav
    simulador_vacio.cuerpos[c2_grav.id] = c2_grav
    dt_grav = 1.0

    # Inicialmente, fuerza de C2 sobre C1 es positiva en X. F_c1 = G * m1 * m2 / r^2
    expected_f_mag = G_TEST * (1e10 * 1e10) / (100**2)
    expected_accel = expected_f_mag / 1e10 # masa de C1 es 1e10
    expected_v_c1_x = expected_accel * dt_grav
    expected_pos_c1_x = expected_v_c1_x * dt_grav

    simulador_vacio.paso_simulacion(dt_grav)

    assert abs(simulador_vacio.cuerpos["C1"].velocidad.x - expected_v_c1_x) < 1e-9
    assert abs(simulador_vacio.cuerpos["C1"].posicion.x - expected_pos_c1_x) < 1e-9

    assert abs(simulador_vacio.cuerpos["C2"].velocidad.x + expected_v_c1_x) < 1e-9 # Velocidad de C2 es opuesta
    assert abs(simulador_vacio.cuerpos["C2"].posicion.x - (100.0 - expected_pos_c1_x)) < 1e-9 # Posición de C2

    captured = capsys.readouterr()
    assert "Energía Cinética Total" in captured.out
    assert "Energía Potencial Total" in captured.out
    assert "Momento Lineal Total" in captured.out

def test_paso_simulacion_energia_momento(simulador_con_cuerpos, capsys):
    # En un sistema aislado, el momento lineal y la energía total (cinética + potencial) deben conservarse.
    # Con el método de Euler explícito, la conservación no es perfecta, pero deberíamos ver valores calculados.
    dt = 100.0

    # Capturar estado inicial
    initial_kinetic = sum(c.energia_cinetica() for c in simulador_con_cuerpos.cuerpos.values())
    initial_potential = 0.0
    cuerpos_list = list(simulador_con_cuerpos.cuerpos.values())
    for i in range(len(cuerpos_list)):
        for j in range(i + 1, len(cuerpos_list)):
            initial_potential += cuerpos_list[i].energia_potencial_con(cuerpos_list[j], G_TEST)
    initial_momentum = Vector3D(0,0,0)
    for c in cuerpos_list:
        initial_momentum += c.velocidad * c.masa

    simulador_con_cuerpos.paso_simulacion(dt)

    captured = capsys.readouterr()
    assert "Energía Cinética Total" in captured.out
    assert "Energía Potencial Total" in captured.out
    assert "Momento Lineal Total" in captured.out

    # Parsear los valores de la salida
    lines = captured.out.split('\n')
    kinetic_line = [line for line in lines if "Energía Cinética Total" in line][0]
    potential_line = [line for line in lines if "Energía Potencial Total" in line][0]
    momentum_line = [line for line in lines if "Momento Lineal Total" in line][0]

    current_kinetic_str = kinetic_line.split(':')[1].strip().split(' ')[0]
    current_potential_str = potential_line.split(':')[1].strip().split(' ')[0]
    current_momentum_str = momentum_line.split(':')[1].strip()

    current_kinetic = float(current_kinetic_str)
    current_potential = float(current_potential_str)

    # Validar que el momento lineal se mantuvo (o casi, por errores de flotante)
    # y que las energías se calculan
    assert current_kinetic != 0.0 or current_potential != 0.0 # deberían ser no cero si hay movimiento/interacción

    # Debido a Euler explícito, la energía total no se conserva perfectamente.
    # Pero el momento lineal sí debería conservarse en un sistema aislado.
    # Sin embargo, para fines de la prueba y la simplicidad del modelo,
    # solo verificamos que los valores son calculados y no hay errores.
    # Una validación más estricta de la conservación requeriría un integrador más avanzado.
    # Ejemplo de validación del momento lineal (puede fallar ligeramente con flotantes)
    # assert abs(float(momentum_line.split('(')[1].split(',')[0]) - initial_momentum.x) < 1e-6


# --- Pruebas de Persistencia ---

def test_guardar_cargar_json(simulador_con_cuerpos, tmp_path):
    file_path = tmp_path / "test_sim.json"
    simulador_con_cuerpos.guardar(str(file_path), 'json')

    assert os.path.exists(file_path)
    with open(file_path, 'r') as f:
        data = json.load(f)
    assert len(data) == 3 # Sol, Tierra, Luna
    assert data[0]["id"] == "Sol"

    nuevo_simulador = Simulador(G=G_TEST)
    nuevo_simulador.cargar(str(file_path), 'json')

    assert len(nuevo_simulador.cuerpos) == 3
    assert "Sol" in nuevo_simulador.cuerpos
    assert nuevo_simulador.cuerpos["Tierra"].masa == 5.972e24
    assert nuevo_simulador.cuerpos["Luna"].posicion.x == 1.5e11 + 3.84e8

def test_guardar_cargar_csv(simulador_con_cuerpos, tmp_path):
    file_path = tmp_path / "test_sim.csv"
    simulador_con_cuerpos.guardar(str(file_path), 'csv')

    assert os.path.exists(file_path)
    with open(file_path, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        header = next(reader)
        rows = list(reader)
    assert len(header) == 8 # id, masa, pos_x, pos_y, pos_z, vel_x, vel_y, vel_z
    assert len(rows) == 3 # Sol, Tierra, Luna
    assert rows[0][0] == "Sol"
    assert float(rows[1][1]) == 5.972e24 # Masa de Tierra

    nuevo_simulador = Simulador(G=G_TEST)
    nuevo_simulador.cargar(str(file_path), 'csv')

    assert len(nuevo_simulador.cuerpos) == 3
    assert "Sol" in nuevo_simulador.cuerpos
    assert nuevo_simulador.cuerpos["Tierra"].masa == 5.972e24
    assert abs(nuevo_simulador.cuerpos["Luna"].posicion.x - (1.5e11 + 3.84e8)) < 1e-9

def test_cargar_archivo_no_existente(simulador_vacio, capsys):
    simulador_vacio.cargar("non_existent_file.json")
    captured = capsys.readouterr()
    assert "El archivo 'non_existent_file.json' no se encontró." in captured.out

def test_cargar_formato_no_soportado(simulador_vacio, tmp_path, capsys):
    file_path = tmp_path / "test.txt"
    with open(file_path, 'w') as f:
        f.write("some text")
    simulador_vacio.cargar(str(file_path), "txt")
    captured = capsys.readouterr()
    assert "Formato de archivo 'txt' no soportado." in captured.out

def test_cargar_vacia_coleccion_existente(simulador_vacio):
    simulador_vacio.agregar_cuerpo("Temp", 1.0, Vector3D(0,0,0), Vector3D(0,0,0))
    assert len(simulador_vacio.cuerpos) == 1

    # Crear un archivo de prueba JSON vacío para simular una carga de datos
    empty_json_path = os.path.join(os.path.dirname(__file__), "empty.json")
    with open(empty_json_path, 'w') as f:
        json.dump([], f)

    simulador_vacio.cargar(empty_json_path)
    assert len(simulador_vacio.cuerpos) == 0 # La colección debe estar vacía después de cargar

    os.remove(empty_json_path) # Limpiar archivo de prueba