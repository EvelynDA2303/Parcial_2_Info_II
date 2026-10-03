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

# Elegimos la condicion 1 para probar el filtro
datos_condicion = archivo.seleccionar_condicion(1)

# Revisamos las primeras filas y las condiciones que quedaron
print("\nDatos de la condicion seleccionada")
print(datos_condicion.head())

print("\nCondiciones presentes")
print(datos_condicion["condition"].unique())

print("\nCantidad de filas seleccionadas")
print(len(datos_condicion))