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