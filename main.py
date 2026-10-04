# Importamos la clase del CSV y la funcion que revisa los numeros
from clases import ArchivoCSV, leer_entero


def elegir_condicion():
    # Mostramos las condiciones que se pueden analizar
    print("\nCondiciones disponibles: 1, 2 y 3")

    # Pedimos una condicion y revisamos que sea valida
    return leer_entero("Selecciona la condicion: ", 1, 3)


def elegir_canal(archivo, mensaje):
    # Estos son los nombres de los canales de los archivos ERP
    canales_validos = [
        "Fz", "FCz", "Cz", "FC3", "FC4",
        "C3", "C4", "CP3", "CP4"
    ]

    # Guardamos solamente los canales que aparecen en el archivo
    canales = []

    for canal in canales_validos:
        if canal in archivo.datos.columns:
            canales.append(canal)

    # Avisamos si no encontramos ningun canal conocido
    if not canales:
        raise ValueError("El archivo no tiene canales reconocidos")

    # Mostramos cada canal con un numero para elegirlo
    print("\nCanales disponibles")

    for numero, canal in enumerate(canales, start=1):
        print(f"{numero} - {canal}")

    # Revisamos que el numero elegido aparezca en la lista
    opcion = leer_entero(mensaje, 1, len(canales))

    # Restamos uno porque las posiciones de la lista empiezan en cero
    return canales[opcion - 1]


def menu_csv():
    # Al comenzar no tenemos ningun archivo cargado
    archivo = None

    # Mantenemos el menu activo hasta elegir salir
    while True:
        print("\n========== MENU CSV ==========")

        # Mostramos el archivo con el que estamos trabajando
        if archivo is not None:
            print(f"Archivo actual: {archivo.ruta}")

        print("1 - Cargar archivo CSV")
        print("2 - Mostrar informacion del archivo")
        print("3 - Crear y guardar graficas")
        print("4 - Calcular diferencia entre canales")
        print("0 - Salir")

        # Pedimos una opcion valida del menu
        opcion = leer_entero("Selecciona una opcion: ", 0, 4)

        # Terminamos el ciclo cuando la persona elige cero
        if opcion == 0:
            print("Menu CSV finalizado")
            break

        if opcion == 1:
            # Quitamos espacios y comillas alrededor de la ruta
            ruta = input(
                "\nNombre o ruta del archivo CSV: "
            ).strip().strip('"')

            try:
                # Leemos el nuevo archivo sin reemplazar aun el anterior
                nuevo_archivo = ArchivoCSV(ruta)

                # Colocamos el tiempo como indice de las filas
                nuevo_archivo.establecer_indice_tiempo()

                # Revisamos que exista la columna de las condiciones
                if "condition" not in nuevo_archivo.datos.columns:
                    raise ValueError(
                        "El archivo no tiene la columna condition"
                    )

                # Usamos el nuevo archivo cuando termina la revision
                archivo = nuevo_archivo
                print("Archivo CSV cargado correctamente")

            except (OSError, ValueError) as error:
                # Mostramos el problema sin cerrar el programa
                print(f"No se pudo cargar el archivo: {error}")

            # Volvemos al menu despues de intentar cargar el archivo
            continue

        # Evitamos hacer calculos cuando todavia no hay datos
        if archivo is None:
            print("Primero debes cargar un archivo con la opcion 1")
            continue

        try:
            if opcion == 2:
                # Al imprimir el objeto se ejecuta su metodo __str__
                print(archivo)

            elif opcion == 3:
                # Elegimos la condicion que queremos analizar
                condicion = elegir_condicion()

                # Usamos este canal para el stem y el histograma
                print("\nCanal para el stem y el histograma")
                canal = elegir_canal(
                    archivo, "Selecciona el canal: "
                )

                # Elegimos el canal del eje horizontal del scatter
                print("\nCanal para el eje X del scatter")
                canal_x = elegir_canal(
                    archivo, "Selecciona el canal X: "
                )

                # Elegimos el canal del eje vertical del scatter
                print("\nCanal para el eje Y del scatter")
                canal_y = elegir_canal(
                    archivo, "Selecciona el canal Y: "
                )

                # Pedimos otro canal si se eligio el mismo en ambos ejes
                while canal_y == canal_x:
                    print("Elige un canal diferente al del eje X")
                    canal_y = elegir_canal(
                        archivo, "Selecciona el canal Y: "
                    )

                # Pedimos el nombre con el que se guardara la imagen
                nombre_imagen = input(
                    "\nNombre para la imagen incluyendo .png o .jpg: "
                ).strip()

                # Usamos este nombre si no se escribe ninguno
                if not nombre_imagen:
                    nombre_imagen = "grafica_csv.png"

                # Agregamos la extension si no tiene una de las permitidas
                if not nombre_imagen.lower().endswith(
                    (".png", ".jpg", ".jpeg")
                ):
                    nombre_imagen += ".png"

                # La ventana debe cerrarse para continuar con el menu
                print("\nCierra la ventana de la grafica para continuar")

                # Creamos y guardamos las tres graficas con la clase CSV
                archivo.graficar(
                    condicion,
                    canal,
                    canal_x,
                    canal_y,
                    nombre_imagen
                )

                print(f"Imagen guardada en: {nombre_imagen}")

            elif opcion == 4:
                # Elegimos la condicion para mostrar la diferencia
                condicion = elegir_condicion()

                # Aclaramos el orden porque cambia el signo del resultado
                print("\nCalcularemos canal A menos canal B")
                print("Puedes probar con C3 y C4")

                # Pedimos los dos canales que vamos a restar
                canal_a = elegir_canal(
                    archivo, "Selecciona el canal A: "
                )
                canal_b = elegir_canal(
                    archivo, "Selecciona el canal B: "
                )

                # Evitamos restar un canal consigo mismo
                while canal_b == canal_a:
                    print("Elige un canal diferente al canal A")
                    canal_b = elegir_canal(
                        archivo, "Selecciona el canal B: "
                    )

                # Creamos la columna y recibimos la condicion seleccionada
                resultado = archivo.crear_diferencia(
                    condicion, canal_a, canal_b
                )

                # Mostramos una parte para no llenar toda la terminal
                print(
                    f"\nPrimeras 10 filas de {canal_a} menos {canal_b}"
                )
                print("Valores en microvoltios")
                print(resultado.head(10).to_string())

                # Indicamos cuantos registros tiene el resultado completo
                print(f"\nCantidad de filas del resultado: {len(resultado)}")

                # La columna queda en memoria y no cambia el CSV original
                print("La diferencia quedo en una nueva columna de la tabla")
                print("El archivo CSV original no fue modificado")

        except (OSError, ValueError) as error:
            # Si hay un problema avisamos y dejamos usar otra opcion
            print(f"No se pudo realizar la operacion: {error}")


# Iniciamos el menu solo cuando ejecutamos este archivo directamente
if __name__ == "__main__":
    menu_csv()