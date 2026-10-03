import pandas as pd
from io import StringIO


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