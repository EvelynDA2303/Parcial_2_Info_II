from clases import ArchivoMAT


# Cargamos el archivo y mostramos su informacion
archivo = ArchivoMAT("Sensitive_Cue.mat")
print(archivo)

# Seleccionamos la variable que contiene los datos
archivo.seleccionar_matriz("Sensitive")

print("Variable seleccionada:", archivo.nombre_variable)
print("Forma de la matriz original:", archivo.matriz_3d.shape)

# Convertimos los datos a 2D y mostramos las dos formas
archivo.convertir_a_2d()

print("Forma de la matriz 2D:", archivo.matriz_2d.shape)
print("Forma de la matriz original:", archivo.matriz_3d.shape)