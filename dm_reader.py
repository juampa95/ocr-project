import os
import pathlib
import cv2
import pylibdmtx.pylibdmtx as dmtx
import numpy as np

ruta_imagen = 'test/img2/20230615131504.bmp'

# DETECTAR Y DECODIFICAR DM
def det_dm(imagen):
    img = cv2.imread(imagen,cv2.IMREAD_GRAYSCALE)
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w > 10 and h > 10:
            dm_region = img[y:y + h, x:x + w]
            mensaje = dmtx.decode(dm_region)
            print(dm_region)
            if mensaje:
                return mensaje[0].data.decode("utf-8")
    return None

mensaje_dm = det_dm(ruta_imagen)

if mensaje_dm:
    print('mensaje: ',mensaje_dm)
else:
    print('No hay dm')

# RESULTADO
# Bueno pero muy lento. No me sirve para detectar lineas de texto
