from clases import ArchivoMAT
import scipy.io as sio

archivo = ArchivoMAT("Sensitive_Cue.mat")

print("Variables del archivo:")
print(sio.whosmat(archivo.ruta))

print("Dimensiones de la matriz:")
print(archivo.datos["Sensitive"].shape)
