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

# Copiar la imagen para dibujar el rectángulo en la imagen original
drawing = img.copy()

# Establecer las coordenadas del rectángulo (esquina superior izquierda y esquina inferior derecha)
x1, y1 = 22, 147  # Coordenadas de la esquina superior izquierda
x2, y2 = 349, 610  # Coordenadas de la esquina inferior derecha

# Establecer el color y el grosor del contorno del rectángulo
color = (255, 255, 255)  # Rectángulo verde
grosor = 2

# Dibujar el rectángulo en la imagen
cv2.rectangle(drawing, (349, 610), (349+147, 610+22), color, grosor)

# see the results
cv2.imshow('None approximation', drawing)
cv2.waitKey(0)
cv2.destroyAllWindows()
