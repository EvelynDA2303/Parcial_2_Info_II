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

# Probamos la seleccion de cuatro canales y sus primeras 250 muestras
canales = [0, 1, 2, 3]
segmento = archivo.seleccionar_segmento(canales, 0, 250)

print("Canales seleccionados:", canales)
print("Forma del segmento:", segmento.shape)