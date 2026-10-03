import scipy.io as sio


class ArchivoMAT:
    def __init__(self, ruta):
        self.ruta = ruta
        self.datos = sio.loadmat(ruta)