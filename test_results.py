import pytesseract
import time

# Prueba modelo best 
ruta_imagen = '/home/jpmanzano/ocr-project/test/priv_img/TEST280623/20230615131714.bmp'  # Ruta a la imagen que deseas procesar
ruta_modelo = '/home/jpmanzano/ocr-project/tesstrain/data/'  # Ruta a la carpeta que contiene el modelo entrenado

inicio = time.time()
texto = pytesseract.image_to_string(ruta_imagen, config=f'--tessdata-dir "{ruta_modelo}" -l ocrafast')
tiempo_transcurrido = time.time() - inicio


print("Texto extraído best: ", texto)
print("Tiempo de ejecución best: ",tiempo_transcurrido)


# Prueba modelo fast
ruta_modelo = '/home/jpmanzano/ocr-project/tesstrain/data/ocrafast/tessdata_fast/'  # Ruta a la carpeta que contiene el modelo entrenado

inicio = time.time()
texto = pytesseract.image_to_string(ruta_imagen, config=f'--tessdata-dir "{ruta_modelo}" -l ocrafast_0.010000_106_1800')
tiempo_transcurrido = time.time() - inicio


print("Texto extraído fast: ", texto)
print("Tiempo de ejecución fast: ",tiempo_transcurrido)

