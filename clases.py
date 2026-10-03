import pandas as pd


class ArchivoCSV:
    def __init__(self, ruta):
        self.ruta = ruta
        self.datos = pd.read_csv(ruta)