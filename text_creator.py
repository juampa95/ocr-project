import random

caracteres = "ABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890/\:()"  # Caracteres disponibles (sin espacio)
cantidad_caracteres = 500000  # Cantidad de caracteres a generar
caracteres_por_linea = 50  # Cantidad de caracteres por línea

texto_aleatorio = ''.join(random.choice(caracteres) for _ in range(cantidad_caracteres))

nombre_archivo = "ocra2.training_text"  # Nombre del archivo de texto
ruta_archivo = "test/" + nombre_archivo  # Ruta completa del archivo de texto

with open(ruta_archivo, "w") as archivo:
    for i in range(0, len(texto_aleatorio), caracteres_por_linea):
        linea = texto_aleatorio[i:i+caracteres_por_linea] + '\n'
        archivo.write(linea)

print(f"Archivo '{nombre_archivo}' creado con éxito en la carpeta '{ruta_archivo}'")