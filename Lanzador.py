from Simulador import Simulador
from Clase_vector_3D import Vector3D
import sys

def mostrar_menu():
    print("\n--- Menú del Simulador de Sistemas Planetarios ---")
    print("1. Listar cuerpos celestes")
    print("2. Agregar nuevo cuerpo celeste")
    print("3. Ejecutar paso de simulación")
    print("4. Guardar simulación")
    print("5. Cargar simulación")
    print("6. Salir")
    print("-------------------------------------------------")

def main():
    simulador = Simulador(G=6.674e-11) # Valor típico de la constante G

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            simulador.listar_cuerpos()
        elif opcion == '2':
            try:
                id_cuerpo = input("ID del cuerpo: ")
                if simulador.obtener_cuerpo(id_cuerpo):
                    print(f"Error: Ya existe un cuerpo con el ID '{id_cuerpo}'.")
                    continue

                masa = float(input("Masa (kg): "))
                pos_x = float(input("Posición X (m): "))
                pos_y = float(input("Posición Y (m): "))
                pos_z = float(input("Posición Z (m): "))
                vel_x = float(input("Velocidad X (m/s): "))
                vel_y = float(input("Velocidad Y (m/s): "))
                vel_z = float(input("Velocidad Z (m/s): "))

                posicion = Vector3D(pos_x, pos_y, pos_z)
                velocidad = Vector3D(vel_x, vel_y, vel_z)
                simulador.agregar_cuerpo(id_cuerpo, masa, posicion, velocidad)
            except ValueError as e:
                print(f"Entrada inválida: {e}. Asegúrese de introducir números para masa, posición y velocidad.")
        elif opcion == '3':
            try:
                dt = float(input("Ingrese el paso de tiempo (dt en segundos): "))
                if dt <= 0:
                    print("El paso de tiempo debe ser positivo.")
                    continue
                simulador.paso_simulacion(dt)
            except ValueError:
                print("Entrada inválida. Ingrese un número para el paso de tiempo.")
        elif opcion == '4':
            nombre_archivo = input("Nombre del archivo para guardar (ej. 'simulacion.json' o 'datos.csv'): ")
            formato = 'json' if nombre_archivo.lower().endswith('.json') else 'csv'
            simulador.guardar(nombre_archivo, formato)
        elif opcion == '5':
            nombre_archivo = input("Nombre del archivo para cargar (ej. 'simulacion.json' o 'datos.csv'): ")
            formato = 'json' if nombre_archivo.lower().endswith('.json') else 'csv'
            simulador.cargar(nombre_archivo, formato)
        elif opcion == '6':
            print("Saliendo del simulador. ¡Hasta luego!")
            sys.exit()
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()