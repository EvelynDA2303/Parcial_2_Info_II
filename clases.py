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

    def establecer_indice_tiempo(self):
        # Revisamos si ya tenemos el tiempo como indice
        if self.datos.index.name == "time_ms":
            return

        # Verificamos que el archivo tenga la columna de tiempo
        if "time_ms" not in self.datos.columns:
            raise ValueError("El archivo no tiene la columna time_ms")

        # Usamos el tiempo en milisegundos como referencia de cada fila
        self.datos = self.datos.set_index("time_ms")