import cv2 as cv
import glob
import numpy as np

class TextRectanglesDetector:
    def __init__(self):
        self.threshold = 60
        self.min_area = 3
        self.max_line_gap = 7  # Distancia verical entre lineas
        self.max_char_gap = 50  # Distancia entre caracteres 
        self.min_char_width = 15
        self.max_char_width = 65
        self.min_char_height = 15
        self.max_char_height = 65
        self.min_total_width = 120
        self.max_total_width = 700
        self.min_total_height = 20
        self.max_total_height = 100
        self.margin = 5

    def detect_rectangles(self,image_path):
        # Leer la imagen de entrada
        src = cv.imread(image_path)

        # Convertir la imagen a escala de grises y aplicar desenfoque
        src_gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
        # src_gray = cv.blur(src_gray, (3, 3))  # procesado anterior, se agregaron los tres pasos siguientes. 

        src_gray = cv.medianBlur(src_gray, 3)

        gamma = 1.0  # Valor del parámetro gamma (puedes ajustarlo según tus necesidades)
        adjusted_image = np.power(src_gray/255.0, gamma)
        adjusted_image = np.uint8(adjusted_image * 255)

        adaptive_threshold = cv.adaptiveThreshold(adjusted_image, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 11, 5)


        # Procesar la imagen
        canny_output = cv.Canny(adaptive_threshold, self.threshold, self.threshold * 2)
        contours, _ = cv.findContours(canny_output, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        rectangles = []

        for i, c in enumerate(contours):
            area = cv.contourArea(c)
            if area > self.min_area:
                x, y, w, h = cv.boundingRect(c)

                if self.min_char_width <= w <= self.max_char_width and self.min_char_height <= h <= self.max_char_height:
                    rectangles.append((x, y, w, h))
        
        for rect in rectangles:  # Esta parte grafica los rectangulos de cada caracter 
            x, y, w, h = rect
            color = (0, 0, 255)
            cv.rectangle(src,(x, y), (x + w, y + h), color, 2)

        # Fusionar los rectángulos de cada línea de texto
        rectangles = self.merge_rectangles(rectangles)

        filtered_rectangles = []

        for rect in rectangles:
            x, y, w, h = rect
            x -= self.margin
            y -= self.margin
            w += 2 * self.margin
            h += 2 * self.margin

            if self.min_total_width <= w <= self.max_total_width and self.min_total_height <= h <= self.max_total_height:
                filtered_rectangles.append(rect)
                color = (255, 0, 0)
                cv.rectangle(src, (x, y), (x + w, y + h), color, 2)

        cv.imshow('Contours', src)
        cv.waitKey()
        cv.destroyAllWindows()


    def merge_rectangles(self, rectangles):
        rectangles = sorted(rectangles, key=lambda r: r[1])  # Ordenar los rectángulos por coordenada Y

        merged_rectangles = []
        current_line = []
        prev_y = None

        for rect in rectangles:
            x, y, w, h = rect

            if prev_y is None or y - prev_y > self.max_line_gap:
                if current_line:
                    merged_rectangles.extend(self.filter_rectangles(current_line))  # Filtrar los rectángulos en la línea
                    current_line = []

            current_line.append(rect)
            prev_y = y

        if current_line:
            merged_rectangles.extend(self.filter_rectangles(current_line))  # Filtrar los rectángulos en la última línea

        return merged_rectangles


    def filter_rectangles(self, rectangles):
        rectangles = sorted(rectangles, key=lambda r: r[0])  # Ordenar los rectángulos por coordenada X

        filtered_rectangles = []
        current_group = []
        prev_x = None

        for rect in rectangles:
            x, y, w, h = rect

            if prev_x is None or x - prev_x <= self.max_char_gap:
                current_group.append(rect)
            else:
                if current_group:
                    filtered_rectangles.append(self.merge_group_rectangles(current_group))  # Fusionar rectángulos en el grupo
                    current_group = [rect]
                else:
                    current_group.append(rect)

            prev_x = x

        if current_group:
            filtered_rectangles.append(self.merge_group_rectangles(current_group))  # Fusionar rectángulos en el último grupo

        return filtered_rectangles


    def merge_group_rectangles(self, group):
        min_x = min(rect[0] for rect in group)
        min_y = min(rect[1] for rect in group)
        max_x = max(rect[0] + rect[2] for rect in group)
        max_y = max(rect[1] + rect[3] for rect in group)

        return (min_x, min_y, max_x - min_x, max_y - min_y)


# Uso de la clase TextRectanglesDetector para una sola imagen
# image_path = 'test/img2/20230615131504.bmp'

# detector = TextRectanglesDetector()
# detector.detect_rectangles(image_path)

################# TEST VARIAS IMAGENES ###################

# Directorio de imágenes
image_dir = 'test/img2/'

# Obtener la lista de archivos .bmp en el directorio  
image_files = glob.glob(image_dir + '*.bmp')

print(image_files)

# Crear el detector de rectángulos de texto
detector = TextRectanglesDetector()

# Procesar cada imagen
for image_file in image_files:
    print('Procesando:', image_file)
    detector.detect_rectangles(image_file)