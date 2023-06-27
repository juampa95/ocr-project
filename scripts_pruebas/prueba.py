import cv2 as cv
import os

# Obtener la ruta completa del script actual
script_path = os.path.abspath(__file__)

# Obtener la ruta del directorio raíz del repositorio
repo_root = os.path.dirname(os.path.dirname(script_path))

ruta_imagen = 'test/priv_img/output/20230615142934_1.tiff'

# Ruta de la imagen recién creada
ruta_imagen = os.path.join(repo_root,ruta_imagen)

# Leer la imagen utilizando OpenCV
img = cv.imread(ruta_imagen)

# Verificar si la imagen se ha leído correctamente
if img is not None:
    # Mostrar la imagen en una ventana
    cv.imshow('Imagen Recortada', img)

    # Esperar hasta que se presione cualquier tecla para cerrar la ventana
    cv.waitKey(0)

    # Cerrar todas las ventanas abiertas
    cv.destroyAllWindows()
else:
    print('No se pudo leer la imagen.')
