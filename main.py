from clases import ArchivoMAT

archivo = ArchivoMAT("Sensitive_Cue.mat")
print(archivo)

archivo.seleccionar_matriz("Sensitive")

print("Variable seleccionada:", archivo.nombre_variable)
print("Forma de la matriz original:", archivo.matriz_3d.shape)