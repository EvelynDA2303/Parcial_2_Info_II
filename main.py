from clases import ArchivoCSV


# Cargamos el CSV para revisar su informacion
archivo = ArchivoCSV("ERP_02.csv")

# Mostramos la informacion general y las estadisticas
print(archivo)

# Ponemos el tiempo como indice de la tabla
archivo.establecer_indice_tiempo()

# Revisamos las primeras filas con el nuevo indice
print("\nTabla con el tiempo como indice")
print(archivo.datos.head())