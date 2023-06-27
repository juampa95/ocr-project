import cv2 as cv
import numpy as np

def thresh_callback(val):
    
    threshold = val
    canny_output = cv.Canny(src_gray, threshold, threshold * 2)
    contours, _ = cv.findContours(canny_output, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
    
    for i, c in enumerate(contours):
        area = cv.contourArea(c)
        if area > min_area:  # Establece un área mínima para filtrar los contornos
            color = (255, 0, 0)
            x, y, w, h = cv.boundingRect(c)
            cv.rectangle(src, (x, y), (x + w, y + h), color, 2)
    
    cv.imshow('Contours', src)

# Leer la imagen de entrada
src = cv.imread('test/img2/20230615131504.bmp')

# Convertir la imagen a escala de grises y aplicar desenfoque
src_gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
src_gray = cv.blur(src_gray, (3, 3))

# Crear ventana y trackbar para ajustar el umbral
cv.namedWindow('Source')
max_thresh = 255
thresh = 100  # Umbral inicial
# Área mínima para filtrar los contornos (ajusta este valor según tus necesidades)
min_area = 12
cv.createTrackbar('Canny thresh:', 'Source', thresh, max_thresh, thresh_callback)

thresh_callback(thresh)
cv.waitKey()
cv.destroyAllWindows()
