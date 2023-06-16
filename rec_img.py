import cv2
import numpy as np

ruta_imagen = 'test/img2/20230615131504.bmp'

img = cv2.imread(ruta_imagen)

src_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

src_gray = cv2.blur(src_gray, (3, 3))

threshold = 40
    
canny_output = cv2.Canny(src_gray, threshold, threshold * 2)
    
contours, _ = cv2.findContours(canny_output, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Crear una copia de la imagen original para dibujar los rectángulos
img_rectangles = img.copy()

# Crear una lista para almacenar los rectángulos delimitadores de los caracteres
bounding_rects = []

# Definir el umbral para distinguir entre palabras y caracteres individuales
umbral_ancho = 0  # Ancho mínimo para considerar una palabra

drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)

# Dibujar los rectángulos alrededor de los contornos y almacenar los rectángulos en la lista
for contour in contours:
    # Obtener las coordenadas del rectángulo delimitador
    x, y, w, h = cv2.boundingRect(contour)

    # Verificar si el rectángulo cumple con el umbral de ancho para considerarlo como una palabra
    if w > umbral_ancho:
        # Dibujar el rectángulo en la imagen
        cv2.rectangle(img_rectangles, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Agregar el rectángulo a la lista de bounding_rects
        bounding_rects.append((x, y, w, h))

# Obtener los límites horizontales y verticales máximos y mínimos de los rectángulos de los caracteres
x_min = min([x for x, y, w, h in bounding_rects])
y_min = min([y for x, y, w, h in bounding_rects])
x_max = max([x + w for x, y, w, h in bounding_rects])
y_max = max([y + h for x, y, w, h in bounding_rects])

# Dibujar el rectángulo que engloba toda la palabra en la imagen original
cv2.rectangle(drawing, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

# Mostrar la imagen con los rectángulos
cv2.namedWindow("Imagen con rectángulos", cv2.WINDOW_NORMAL)
cv2.imshow("Imagen con rectángulos", drawing)
cv2.waitKey(0)
cv2.destroyAllWindows()
