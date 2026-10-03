import scipy.io as sio


class ArchivoMAT:
    def __init__(self, ruta):
        self.ruta = ruta
        self.datos = sio.loadmat(ruta)

    def __str__(self):
        informacion = f"Archivo: {self.ruta}\n"

        for nombre, dimensiones, tipo in sio.whosmat(self.ruta):
            informacion += f"Variable: {nombre}\n"
            informacion += f"Dimensiones: {dimensiones}\n"
            informacion += f"Tipo de dato: {tipo}\n"

        return informacion
    
    def seleccionar_matriz(self, nombre_variable):
        if nombre_variable not in self.datos:
            raise ValueError("La variable no existe en el archivo.")

        matriz = self.datos[nombre_variable]

        if getattr(matriz, "ndim", None) != 3:
            raise ValueError("La variable debe ser una matriz de 3 dimensiones.")

        self.nombre_variable = nombre_variable
        self.matriz_3d = matriz