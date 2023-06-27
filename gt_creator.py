import cv2 as cv
import os
import glob

# ESTE SCRIPT SOLO FUNCIONARA PARA IMAGENES PROPIAS YA QUE CONTIENE INFO SENSIBLE. DEBERA SER ADAPTADO A C/CONJUNTO DE IMAGENES

path_dir ='tesstrain/data/prueba-ground-truth/'
output_dir = 'tesstrain/data/prueba-ground-truth/'

files = glob.glob(path_dir + '*.tif')
files = sorted(files)

num = 23061510012  # Esto corresponde a la parte numerica del nombre, que se incrementara de a 1. Solo cuando el archivo termina en 1

for image_path in files:
    image_name = os.path.basename(image_path)  # Nombre base del archivo
    text_content = ""  # Contenido del archivo de texto

    # Definir el contenido de texto según el nombre de la imagen
    if image_name.endswith("1.tif"):
        text_content = "TES"
        text_content += str(num)
        num += 1
    elif image_name.endswith("2.tif"):
        text_content = "0235869U"
    elif image_name.endswith("3.tif"):
        text_content = "14/01/2023"
    elif image_name.endswith("4.tif"):
        text_content = "25/01/2025"
    
    # Crear el archivo de texto con la extensión .gt.txt
    text_file = image_name.replace(".tif", ".gt.txt")
    text_path = os.path.join(output_dir, text_file)

    # Escribir el contenido en el archivo de texto
    with open(text_path, 'w') as file:
        file.write(text_content)