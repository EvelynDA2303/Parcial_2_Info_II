import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
import scipy.io as sio
import numpy as np


class ArchivoCSV:
    def __init__(self, ruta):
        # Guardamos la ruta y leemos el archivo como una tabla
        self.ruta = ruta
        self.datos = pd.read_csv(ruta)

    def __str__(self):
        # Guardamos en memoria el texto que genera info
        contenido = StringIO()
        self.datos.info(buf=contenido)

        # Organizamos la informacion general del archivo
        informacion = f"Archivo: {self.ruta}\n\n"
        informacion += "Informacion general del CSV\n"
        informacion += contenido.getvalue()

        # Agregamos las estadisticas de las columnas numericas
        estadisticas = self.datos.describe()
        informacion += "\nEstadisticas del CSV\n"
        informacion += estadisticas.to_string()

        return informacion

    def establecer_indice_tiempo(self):
        # Revisamos si ya tenemos el tiempo como indice
        if self.datos.index.name == "time_ms":
            return

        # Verificamos que el archivo tenga la columna de tiempo
        if "time_ms" not in self.datos.columns:
            raise ValueError("El archivo no tiene la columna time_ms")

        # Usamos el tiempo en milisegundos como referencia de cada fila
        self.datos = self.datos.set_index("time_ms")

    def seleccionar_condicion(self, condicion):
        # Revisamos que la condicion sea una de las opciones permitidas
        if type(condicion) != int or condicion not in (1, 2, 3):
            raise ValueError("La condicion debe ser 1, 2 o 3")

        if "condition" not in self.datos.columns:
            raise ValueError("El archivo no tiene la columna condition")

        # Tomamos solo las filas de la condicion elegida
        datos_condicion = self.datos[
            self.datos["condition"] == condicion
        ].copy()

        if datos_condicion.empty:
            raise ValueError("No hay datos para esa condicion")

        return datos_condicion

    def seleccionar_canal(self, condicion, canal):
        # Estos son los canales de los archivos ERP
        canales = ["Fz", "FCz", "Cz", "FC3", "FC4",
                   "C3", "C4", "CP3", "CP4"]

        # Evitamos elegir columnas como subject o condition
        if canal not in canales:
            raise ValueError("El nombre no corresponde a un canal valido")

        if canal not in self.datos.columns:
            raise ValueError("El canal no existe en este archivo")

        # Dejamos el tiempo como indice y filtramos la condicion
        self.establecer_indice_tiempo()
        datos_condicion = self.seleccionar_condicion(condicion)

        # Devolvemos los valores del canal con sus tiempos
        return datos_condicion[canal].copy()

    def graficar(self, condicion, canal, canal_x, canal_y, nombre_imagen):
        # Elegimos la senal y los dos canales que vamos a comparar
        senal = self.seleccionar_canal(condicion, canal)
        senal_x = self.seleccionar_canal(condicion, canal_x)
        senal_y = self.seleccionar_canal(condicion, canal_y)

        # Creamos una figura con un espacio grande arriba y dos abajo
        figura = plt.figure(figsize=(12, 8))

        # Mostramos la senal en el tiempo con un grafico de tallos
        eje1 = figura.add_subplot(2, 2, (1, 2))
        eje1.stem(senal.index, senal.values, markerfmt=".")
        eje1.axvline(
            0, color="red", linestyle="--", label="Tiempo cero"
        )
        eje1.set_title(f"Canal {canal} - Condicion {condicion}")
        eje1.set_xlabel("Tiempo (ms)")
        eje1.set_ylabel("Amplitud (µV)")
        eje1.legend()

        # Contamos cuantas muestras caen en cada intervalo de amplitud
        eje2 = figura.add_subplot(2, 2, 3)
        eje2.hist(senal.values, bins=30, edgecolor="black")
        eje2.set_title(f"Histograma del canal {canal}")
        eje2.set_xlabel("Amplitud (µV)")
        eje2.set_ylabel("Cantidad de muestras")

        # Cada punto compara los dos canales en el mismo instante
        eje3 = figura.add_subplot(2, 2, 4)
        eje3.scatter(senal_x.values, senal_y.values, s=8, alpha=0.5)
        eje3.set_title(f"Relacion entre {canal_x} y {canal_y}")
        eje3.set_xlabel(f"{canal_x} (µV)")
        eje3.set_ylabel(f"{canal_y} (µV)")

        # Ajustamos los espacios y guardamos antes de mostrar la figura
        figura.tight_layout()
        figura.savefig(nombre_imagen, dpi=150)
        plt.show()
        plt.close(figura)

    def crear_diferencia(self, condicion, canal_a, canal_b):
        # Validamos los canales y la condicion con el metodo anterior
        self.seleccionar_canal(condicion, canal_a)
        self.seleccionar_canal(condicion, canal_b)

        # Guardamos la diferencia en una nueva columna de la tabla
        nombre_columna = f"diferencia_{canal_a}_{canal_b}"
        self.datos[nombre_columna] = (
            self.datos[canal_a] - self.datos[canal_b]
        )

        # Devolvemos los datos de la condicion que queremos revisar
        datos_condicion = self.seleccionar_condicion(condicion)

        return datos_condicion[[canal_a, canal_b, nombre_columna]]



class ArchivoMAT:
    def __init__(self, ruta):
        # Guardamos la ruta y cargamos las variables del archivo MAT
        self.ruta = ruta
        self.datos = sio.loadmat(ruta)

    def __str__(self):
        # Organizamos la informacion que aparece al imprimir el objeto
        informacion = f"Archivo: {self.ruta}\n"

        # Consultamos el nombre, las dimensiones y el tipo de cada variable
        for nombre, dimensiones, tipo in sio.whosmat(self.ruta):
            informacion += f"Variable: {nombre}\n"
            informacion += f"Dimensiones: {dimensiones}\n"
            informacion += f"Tipo de dato: {tipo}\n"

        return informacion

    def seleccionar_matriz(self, nombre_variable):
        # Revisamos que la variable elegida exista en el archivo
        if nombre_variable not in self.datos:
            raise ValueError("La variable no existe en el archivo")

        matriz = self.datos[nombre_variable]

        # Revisamos que la matriz tenga tres dimensiones
        # Si no tiene el atributo ndim, getattr devuelve None
        if getattr(matriz, "ndim", None) != 3:
            raise ValueError("La variable debe ser una matriz de 3 dimensiones")

        # Conservamos la matriz original para los calculos en 3D
        self.nombre_variable = nombre_variable
        self.matriz_3d = matriz

    def convertir_a_2d(self):
        # Antes de convertir debemos llamar a seleccionar_matriz
        # Obtenemos los canales, los puntos por ensayo y los ensayos
        canales, puntos, ensayos = self.matriz_3d.shape

        # Dejamos los canales en las filas y unimos los ensayos en las columnas
        # El orden F mantiene juntos los puntos de cada ensayo
        # Usamos una copia para no modificar los datos de la matriz original
        self.matriz_2d = np.reshape(
            self.matriz_3d,
            (canales, puntos * ensayos),
            order="F"
        ).copy()

    def seleccionar_segmento(self, canales, punto_inicial, punto_final):
        # Antes de seleccionar el segmento debemos convertir la matriz a 2D
        total_canales, total_puntos = self.matriz_2d.shape

        # Revisamos que se hayan elegido cuatro canales
        if len(canales) != 4:
            raise ValueError("Debes seleccionar cuatro canales")

        # Comprobamos que los canales sean enteros y esten dentro del rango
        canales_revisados = []

        for canal in canales:
            if type(canal) != int:
                raise ValueError("Los canales deben ser numeros enteros")

            if canal < 0 or canal >= total_canales:
                raise ValueError(
                    f"Los canales deben estar entre 0 y {total_canales - 1}"
                )

            if canal in canales_revisados:
                raise ValueError("Selecciona cuatro canales diferentes")

            canales_revisados.append(canal)

        # Los limites deben ser enteros para usarlos como indices
        if type(punto_inicial) != int or type(punto_final) != int:
            raise ValueError("Los limites deben ser numeros enteros")

        # Revisamos que el intervalo tenga datos y no salga de la matriz
        if punto_inicial < 0 or punto_final > total_puntos:
            raise ValueError(
                f"El intervalo debe estar entre 0 y {total_puntos}"
            )

        if punto_inicial >= punto_final:
            raise ValueError("El punto inicial debe ser menor que el final")

        # Tomamos los cuatro canales dentro del intervalo elegido
        # Incluimos el punto inicial y dejamos por fuera el punto final
        segmento = self.matriz_2d[canales, punto_inicial:punto_final]

        return segmento
