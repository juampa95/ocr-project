import pytesseract
import time

ruta_imagen = '/home/jpmanzano/ocr-project/test/img2/20230615131504.bmp'  # Ruta a la imagen que deseas procesar
ruta_modelo = '/home/jpmanzano/ocr-project/tesstrain/data/'  # Ruta a la carpeta que contiene el modelo entrenado

inicio = time.time()
texto = pytesseract.image_to_string(ruta_imagen, config=f'--tessdata-dir "{ruta_modelo}" -l ocrafast')
tiempo_transcurrido = time.time() - inicio


print("Texto extraído: ", texto)
print("Tiempo de ejecución: ",tiempo_transcurrido)
