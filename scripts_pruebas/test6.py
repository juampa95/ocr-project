import cv2 as cv
import numpy as np

# Función para fusionar los rectángulos de cada línea de texto
def merge_rectangles(rectangles):
    # Ordenar los rectángulos por la coordenada Y y luego por la coordenada X
    rectangles = sorted(rectangles, key=lambda r: (r[1], r[0]))

    merged_rectangles = []
    current_line = []
    prev_y = None

    for rect in rectangles:
        x, y, w, h = rect

        if prev_y is None or y - prev_y > max_line_gap:  # Si hay un salto en la coordenada Y, agregar rectángulos de línea actual a la lista final
            if current_line:
                merged_rectangles.append(merge_line_rectangles(current_line))
                current_line = []

        current_line.append(rect)
        prev_y = y

    if current_line:
        merged_rectangles.append(merge_line_rectangles(current_line))

    return merged_rectangles

# Función para fusionar los rectángulos de una línea de texto en un solo rectángulo
def merge_line_rectangles(rectangles):
    min_x = min(rect[0] for rect in rectangles)
    min_y = min(rect[1] for rect in rectangles)
    max_x = max(rect[0] + rect[2] for rect in rectangles)
    max_y = max(rect[1] + rect[3] for rect in rectangles)

    return (min_x, min_y, max_x - min_x, max_y - min_y)

# Función de callback para procesar la imagen
def process_image():
    canny_output = cv.Canny(src_gray, threshold, threshold * 2)
    contours, _ = cv.findContours(canny_output, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    rectangles = []

    for i, c in enumerate(contours):
        area = cv.contourArea(c)
        if area > min_area:  # Establece un área mínima para filtrar los contornos
            x, y, w, h = cv.boundingRect(c)

            # Verificar el ancho y alto del rectángulo de los caracteres
            if min_char_width <= w <= max_char_width and min_char_height <= h <= max_char_height:
                rectangles.append((x, y, w, h))

    merged_rectangles = merge_rectangles(rectangles)

    filtered_rectangles = []

    for rect in merged_rectangles:
        x, y, w, h = rect

        # Añadir un margen adicional a los rectángulos finales
        x -= margin
        y -= margin
        w += 2 * margin
        h += 2 * margin

        # Verificar las dimensiones totales del rectángulo final
        if min_total_width <= w <= max_total_width and min_total_height <= h <= max_total_height:
            filtered_rectangles.append(rect)
            color = (255, 0, 0)
            cv.rectangle(src, (x, y), (x + w, y + h), color, 2)

    cv.imshow('Contours', src)

# Leer la imagen de entrada
src = cv.imread('test/img2/20230615131504.bmp')

# Convertir la imagen a escala de grises y aplicar desenfoque
src_gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
src_gray = cv.blur(src_gray, (3, 3))

# Parámetros modificables caracteres
threshold = 100  # Umbral inicial
min_area = 15  # Área mínima para filtrar los contornos
max_line_gap = 3  # Brecha máxima permitida entre líneas de texto
min_char_width = 20  # Ancho mínimo de los rectángulos de caracteres
max_char_width = 40  # Ancho máximo de los rectángulos de caracteres
min_char_height = 20  # Alto mínimo de los rectángulos de caracteres
max_char_height = 200  # Alto máximo de los rectángulos de caracteres

# Parámetros modificables rectángulos finales
min_total_width = 60  # Ancho mínimo de los rectángulos finales
max_total_width = 3000  # Ancho máximo de los rectángulos finales
min_total_height = 20  # Alto mínimo de los rectángulos finales
max_total_height = 100  # Alto máximo de los rectángulos finales
margin = 5

# Procesar la imagen
process_image()

cv.waitKey()
cv.destroyAllWindows()
