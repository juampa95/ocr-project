import os
import pathlib
import cv2
import numpy as np

ruta_imagen = 'test/img2/20230615131504.bmp'

# Cargar la imagen utilizando OpenCV sin realizar la conversión a escala de grises
img = cv2.imread(ruta_imagen, cv2.IMREAD_UNCHANGED)

# Establecer un umbral
thresh = 50

# Obtener la imagen umbralizada
ret, thresh_img = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)

# Encontrar los contornos
contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# Crear una imagen vacía para dibujar los contornos
img_contours = np.zeros(img.shape)

image_copy = img.copy()
cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(255, 0, 0), thickness=2, lineType=cv2.LINE_AA)

# see the results
cv2.imshow('None approximation', image_copy)
cv2.waitKey(0)
cv2.destroyAllWindows()

# ----------------------------------------------------------------

# Crear una copia de la imagen original para dibujar los rectángulos
img_rectangles = img.copy()

# Dibujar los rectángulos alrededor de los contornos
for contour in contours:
    # Obtener las coordenadas del rectángulo delimitador
    x, y, w, h = cv2.boundingRect(contour)

    # Dibujar el rectángulo en la imagen
    cv2.rectangle(img_rectangles, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Mostrar la imagen con los rectángulos
cv2.imshow("Imagen con rectángulos", img_rectangles)
cv2.waitKey(0)
cv2.destroyAllWindows()
