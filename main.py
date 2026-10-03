from clases import ArchivoCSV, ArchivoMAT


# Probamos el canal Fz de la condicion 1 del CSV
archivo_csv = ArchivoCSV("ERP_02.csv")
print(archivo_csv)

senal = archivo_csv.seleccionar_canal(1, "Fz")

print("\nPrimeros valores del canal Fz")
print(senal.head())

print("\nCantidad de muestras")
print(len(senal))


# Cargamos el MAT y revisamos su informacion
archivo_mat = ArchivoMAT("Sensitive_Cue.mat")
print("\nInformacion del archivo MAT")
print(archivo_mat)

# Elegimos la matriz y conservamos sus dimensiones originales
archivo_mat.seleccionar_matriz("Sensitive")

print("\nDimensiones originales")
print(archivo_mat.matriz_3d.shape)

# Convertimos la matriz para seleccionar un segmento
archivo_mat.convertir_a_2d()

print("\nDimensiones en 2D")
print(archivo_mat.matriz_2d.shape)

segmento = archivo_mat.seleccionar_segmento([0, 1, 2, 3], 0, 250)

print("\nDimensiones del segmento")
print(segmento.shape)

# Graficamos Fz y comparamos los canales C3 y C4
archivo_csv.graficar(
    1, "Fz", "C3", "C4", "ERP_02_condicion1.png"
)

# Calculamos C3 menos C4 y revisamos la condicion 1
resultado = archivo_csv.crear_diferencia(1, "C3", "C4")

print("\nDiferencia entre C3 y C4 en microvoltios")
print(resultado.head())