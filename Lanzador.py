from Simulador import Simulador
from Clase_vector_3D import Vector3D
import sys

class Lanzador:
    def __init__(self, simulador: Simulador):
        self.simulador = simulador

    def mostrar_menu(self):
        print("\n--- Menú del Simulador de Sistemas Planetarios ---")
        print("1. Listar cuerpos celestes")
        print("2. Agregar nuevo cuerpo celeste")
        print("3. Ejecutar paso de simulación")
        print("4. Guardar simulación")
        print("5. Cargar simulación")
        print("6. Salir")
        print("-------------------------------------------------")

    def ejecutar_opcion(self, opcion: str):
        if opcion == '1':
            self.simulador.listar_cuerpos()
        elif opcion == '2':
            self._agregar_cuerpo_interactivo()
        elif opcion == '3':
            self._ejecutar_paso_simulacion_interactivo()
        elif opcion == '4':
            self._guardar_simulacion_interactivo()
        elif opcion == '5':
            self._cargar_simulacion_interactivo()
        elif opcion == '6':
            print("Saliendo del simulador. ¡Hasta luego!")
            sys.exit()
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

    def _agregar_cuerpo_interactivo(self):
        try:
            id_cuerpo = input("ID del cuerpo: ")
            if self.simulador.obtener_cuerpo(id_cuerpo):
                print(f"Error: Ya existe un cuerpo con el ID '{id_cuerpo}'.")
                return

            masa = float(input("Masa (kg): "))
            pos_x = float(input("Posición X (m): "))
            pos_y = float(input("Posición Y (m): "))
            pos_z = float(input("Posición Z (m): "))
            vel_x = float(input("Velocidad X (m/s): "))
            vel_y = float(input("Velocidad Y (m/s): "))
            vel_z = float(input("Velocidad Z (m/s): "))

            posicion = Vector3D(pos_x, pos_y, pos_z)
            velocidad = Vector3D(vel_x, vel_y, vel_z)
            self.simulador.agregar_cuerpo(id_cuerpo, masa, posicion, velocidad)
        except ValueError as e:
            print(f"Entrada inválida: {e}. Asegúrese de introducir números para masa, posición y velocidad.")

    def _ejecutar_paso_simulacion_interactivo(self):
        try:
            dt = float(input("Ingrese el paso de tiempo (dt en segundos): "))
            if dt <= 0:
                print("El paso de tiempo debe ser positivo.")
                return
            self.simulador.paso_simulacion(dt)
        except ValueError:
            print("Entrada inválida. Ingrese un número para el paso de tiempo.")

    def _guardar_simulacion_interactivo(self):
        nombre_archivo = input("Nombre del archivo para guardar (ej. 'simulacion.json' o 'datos.csv'): ")
        formato = 'json' if nombre_archivo.lower().endswith('.json') else 'csv'
        self.simulador.guardar(nombre_archivo, formato)

    def _cargar_simulacion_interactivo(self):
        nombre_archivo = input("Nombre del archivo para cargar (ej. 'simulacion.json' o 'datos.csv'): ")
        formato = 'json' if nombre_archivo.lower().endswith('.json') else 'csv'
        self.simulador.cargar(nombre_archivo, formato)