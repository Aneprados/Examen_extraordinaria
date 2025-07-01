from Simulador import Simulador
from Lanzador import Lanzador

def main():
    simulador = Simulador(G=6.674e-11) # Valor típico de la constante G
    cli = Lanzador(simulador)

    # Añadir algunos cuerpos por defecto para empezar, si se desea
    # simulador.agregar_cuerpo("Sol", 1.989e30, Vector3D(0, 0, 0), Vector3D(0, 0, 0))
    # simulador.agregar_cuerpo("Tierra", 5.972e24, Vector3D(1.5e11, 0, 0), Vector3D(0, 3e4, 0))
    # simulador.agregar_cuerpo("Marte", 6.39e23, Vector3D(2.28e11, 0, 0), Vector3D(0, 2.4e4, 0))

    while True:
        cli.mostrar_menu()
        opcion = input("Seleccione una opción: ")
        cli.ejecutar_opcion(opcion)

if __name__ == "__main__":
    main()