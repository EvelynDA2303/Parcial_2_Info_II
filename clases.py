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