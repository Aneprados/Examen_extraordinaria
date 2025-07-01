from .cuerpo import CuerpoCeleste
from .vector3d import Vector3D
import json
import csv
import math

class Simulador:
    def __init__(self, G: float = 6.67430e-11):  # Constante de gravitación universal
        self.cuerpos: dict[str, CuerpoCeleste] = {}
        self.G = G

    def listar_cuerpos(self):
        if not self.cuerpos:
            print("No hay cuerpos celestes registrados en el simulador.")
            return
        print("\n--- Listado de Cuerpos Celestes ---")
        for i, cuerpo in enumerate(self.cuerpos.values()):
            print(f"{i+1}. ID: {cuerpo.id}")
            print(f"   Masa: {cuerpo.masa:.2e} kg")
            print(f"   Posición: {cuerpo.posicion} m")
            print(f"   Velocidad: {cuerpo.velocidad} m/s")
        print("-----------------------------------")

    def agregar_cuerpo(self, id: str, masa: float, posicion: Vector3D, velocidad: Vector3D):
        if id in self.cuerpos:
            raise ValueError(f"Ya existe un cuerpo con el ID '{id}'.")
        try:
            nuevo_cuerpo = CuerpoCeleste(id, masa, posicion, velocidad)
            self.cuerpos[id] = nuevo_cuerpo
            print(f"Cuerpo '{id}' agregado exitosamente.")
        except ValueError as e:
            print(f"Error al agregar cuerpo: {e}")

    def obtener_cuerpo(self, id: str) -> CuerpoCeleste | None:
        return self.cuerpos.get(id)

    def calcular_fuerzas(self) -> dict[str, Vector3D]:
        fuerzas_netas: dict[str, Vector3D] = {c_id: Vector3D(0, 0, 0) for c_id in self.cuerpos}

        cuerpos_lista = list(self.cuerpos.values())
        num_cuerpos = len(cuerpos_lista)

        for i in range(num_cuerpos):
            for j in range(i + 1, num_cuerpos):
                cuerpo1 = cuerpos_lista[i]
                cuerpo2 = cuerpos_lista[j]

                r_vector = cuerpo2.posicion - cuerpo1.posicion
                distancia = r_vector.magnitude()

                if distancia == 0:
                    continue

                fuerza_magnitud = (self.G * cuerpo1.masa * cuerpo2.masa) / (distancia**2)
                fuerza_direccion = r_vector.normalize()

                fuerza_ij = fuerza_direccion * fuerza_magnitud
                fuerza_ji = fuerza_ij * -1.0

                fuerzas_netas[cuerpo1.id] = fuerzas_netas[cuerpo1.id] + fuerza_ij
                fuerzas_netas[cuerpo2.id] = fuerzas_netas[cuerpo2.id] + fuerza_ji
        return fuerzas_netas

    def paso_simulacion(self, dt: float):
        fuerzas = self.calcular_fuerzas()

        for cuerpo_id, fuerza_neta in fuerzas.items():
            cuerpo = self.cuerpos[cuerpo_id]
            cuerpo.aplicar_fuerza(fuerza_neta, dt)

        for cuerpo in self.cuerpos.values():
            cuerpo.mover(dt)

        energia_cinetica_total = sum(cuerpo.energia_cinetica() for cuerpo in self.cuerpos.values())

        energia_potencial_total = 0.0
        cuerpos_lista = list(self.cuerpos.values())
        for i in range(len(cuerpos_lista)):
            for j in range(i + 1, len(cuerpos_lista)):
                cuerpo1 = cuerpos_lista[i]
                cuerpo2 = cuerpos_lista[j]
                energia_potencial_total += cuerpo1.energia_potencial_con(cuerpo2, self.G)

        momento_lineal_total = Vector3D(0, 0, 0)
        for cuerpo in self.cuerpos.values():
            momento_lineal_total += cuerpo.velocidad * cuerpo.masa

        print(f"\n--- Paso de Simulación (dt = {dt} s) ---")
        print(f"Energía Cinética Total: {energia_cinetica_total:.4e} J")
        print(f"Energía Potencial Total: {energia_potencial_total:.4e} J")
        print(f"Momento Lineal Total: {momento_lineal_total} kg·m/s")
        print("------------------------------------------")

    def guardar(self, archivo: str, formato: str = 'json'):
        if not self.cuerpos:
            print("No hay cuerpos para guardar.")
            return

        data_to_save = [cuerpo.to_dict() for cuerpo in self.cuerpos.values()]

        if formato.lower() == 'json':
            with open(archivo, 'w') as f:
                json.dump(data_to_save, f, indent=4)
            print(f"Simulación guardada en '{archivo}' (JSON).")
        elif formato.lower() == 'csv':
            with open(archivo, 'w', newline='') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(['id', 'masa', 'pos_x', 'pos_y', 'pos_z', 'vel_x', 'vel_y', 'vel_z'])
                for cuerpo_data in data_to_save:
                    row = [
                        cuerpo_data['id'],
                        cuerpo_data['masa'],
                        cuerpo_data['posicion'][0],
                        cuerpo_data['posicion'][1],
                        cuerpo_data['posicion'][2],
                        cuerpo_data['velocidad'][0],
                        cuerpo_data['velocidad'][1],
                        cuerpo_data['velocidad'][2]
                    ]
                    writer.writerow(row)
            print(f"Simulación guardada en '{archivo}' (CSV).")
        else:
            print(f"Formato de archivo '{formato}' no soportado. Use 'json' o 'csv'.")

    def cargar(self, archivo: str, formato: str = 'json'):
        self.cuerpos.clear()

        loaded_data = []
        try:
            if formato.lower() == 'json':
                with open(archivo, 'r') as f:
                    loaded_data = json.load(f)
            elif formato.lower() == 'csv':
                with open(archivo, 'r', newline='') as f:
                    reader = csv.reader(f, delimiter=';')
                    header = next(reader)
                    for row in reader:
                        if len(row) != 8:
                            print(f"Advertencia: Fila CSV mal formada, saltando: {row}")
                            continue

                        try:
                            id = row[0]
                            masa = float(row[1])
                            posicion = [float(row[2]), float(row[3]), float(row[4])]
                            velocidad = [float(row[5]), float(row[6]), float(row[7])]
                            loaded_data.append({
                                "id": id,
                                "masa": masa,
                                "posicion": posicion,
                                "velocidad": velocidad
                            })
                        except ValueError as e:
                            print(f"Error de conversión en fila CSV, saltando: {row}. Error: {e}")
                            continue
            else:
                print(f"Formato de archivo '{formato}' no soportado. Use 'json' o 'csv'.")
                return
        except FileNotFoundError:
            print(f"El archivo '{archivo}' no se encontró.")
            return
        except json.JSONDecodeError:
            print(f"Error al decodificar JSON desde '{archivo}'.")
            return
        except Exception as e:
            print(f"Ocurrió un error inesperado al cargar el archivo: {e}")
            return

        for data in loaded_data:
            try:
                cuerpo = CuerpoCeleste.from_dict(data)
                self.cuerpos[cuerpo.id] = cuerpo
            except ValueError as e:
                print(f"Error al cargar cuerpo '{data.get('id', 'N/A')}' desde el archivo: {e}")
        print(f"Simulación cargada desde '{archivo}'. Se cargaron {len(self.cuerpos)} cuerpos.")