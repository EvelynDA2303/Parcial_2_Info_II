from pathlib import Path
from clases import ArchivoMAT, leer_entero
from clases import sumar_canales, restar_canales, multiplicar_canales


def menu_mat():
    # Al comenzar no tenemos ningun archivo cargado
    archivo = None

    # Mantenemos el menu activo hasta elegir salir
    while True:
        print("\nMENU DE ARCHIVOS MAT")
        print("1 Cargar un archivo MAT")
        print("2 Mostrar informacion del archivo")
        print("3 Operar y graficar cuatro canales")
        print("4 Calcular y graficar estadisticas")
        print("0 Salir")

        opcion = leer_entero("Elige una opcion: ", 0, 4)

        if opcion == 0:
            break

        try:
            if opcion == 1:
                # Permitimos escribir un nombre o una ruta completa
                ruta = input("Nombre o ruta del archivo MAT: ").strip()
                ruta = ruta.strip('"')

                # Revisamos las variables antes de seleccionar la matriz
                nuevo_archivo = ArchivoMAT(ruta)
                print(nuevo_archivo)

                variable = input("Nombre de la variable 3D: ").strip()
                nuevo_archivo.seleccionar_matriz(variable)

                # Cambiamos el archivo activo solo si la carga fue correcta
                archivo = nuevo_archivo
                print("Archivo y matriz seleccionados correctamente")

            elif archivo is None:
                print("Primero debes cargar un archivo con la opcion 1")

            elif opcion == 2:
                print(archivo)

            elif opcion == 3:
                # Elegimos la funcion que recibira el metodo de la clase
                print("\n1 Suma")
                print("2 Resta")
                print("3 Multiplicacion")
                eleccion = leer_entero("Elige la operacion: ", 1, 3)

                if eleccion == 1:
                    operacion = sumar_canales
                    nombre_operacion = "suma"
                elif eleccion == 2:
                    operacion = restar_canales
                    nombre_operacion = "resta"
                else:
                    operacion = multiplicar_canales
                    nombre_operacion = "producto"

                # Consultamos los limites reales de la matriz seleccionada
                archivo.convertir_a_2d()
                total_canales, total_puntos = archivo.matriz_2d.shape

                if total_canales < 4:
                    print("La matriz debe tener al menos cuatro canales")
                    continue

                # Pedimos cuatro canales diferentes y conservamos su orden
                canales = []
                print(f"Canales disponibles: 0 hasta {total_canales - 1}")

                while len(canales) < 4:
                    canal = leer_entero(
                        f"Canal numero {len(canales) + 1}: ",
                        0,
                        total_canales - 1
                    )

                    if canal in canales:
                        print("Ese canal ya fue elegido")
                    else:
                        canales.append(canal)

                # El limite final no se incluye en el segmento
                inicio = leer_entero(
                    "Muestra inicial: ", 0, total_puntos - 1
                )
                final = leer_entero(
                    "Limite final sin incluir: ", inicio + 1, total_puntos
                )

                # Construimos un nombre que identifica el archivo y la prueba
                base = Path(archivo.ruta).stem
                texto_canales = "_".join(str(canal) for canal in canales)

                nombre_imagen = (
                    f"{base}_{archivo.nombre_variable}_{nombre_operacion}"
                    f"_canales_{texto_canales}_muestras_{inicio}_{final}.png"
                )

                archivo.graficar_operacion(
                    operacion, canales, inicio, final, nombre_imagen
                )
                print(f"Imagen guardada en: {nombre_imagen}")

            elif opcion == 4:
                # Explicamos que representa cada eje antes de elegirlo
                print("\nEje 0: canales")
                print("Eje 1: muestras")
                print("Eje 2: ensayos")

                eje_a = leer_entero("Primer eje: ", 0, 2)
                eje_b = leer_entero("Segundo eje: ", 0, 2)

                while eje_a == eje_b:
                    print("Los ejes deben ser diferentes")
                    eje_b = leer_entero("Segundo eje: ", 0, 2)

                # Incluimos los ejes elegidos en el nombre de la imagen
                base = Path(archivo.ruta).stem
                nombre_imagen = (
                    f"{base}_{archivo.nombre_variable}"
                    f"_estadisticas_ejes_{eje_a}_{eje_b}.png"
                )

                archivo.graficar_estadisticas(
                    eje_a, eje_b, nombre_imagen
                )
                print(f"Imagen guardada en: {nombre_imagen}")

        except (OSError, ValueError, NotImplementedError) as error:
            # Mostramos el problema y permitimos volver a intentar
            print(f"No se pudo completar la opcion: {error}")


# Iniciamos el menu cuando ejecutamos este archivo
if __name__ == "__main__":
    menu_mat()