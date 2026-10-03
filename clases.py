import scipy.io as sio
import numpy as np


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