import cv2 as cv
import glob

class TextRectanglesDetector:
    def __init__(self):
        self.threshold = 70
        self.min_area = 15
        self.max_line_gap = 3  # Distancia verical entre lineas
        self.max_char_gap = 50  # Distancia entre caracteres 
        self.min_char_width = 18
        self.max_char_width = 50
        self.min_char_height = 20
        self.max_char_height = 50
        self.min_total_width = 60
        self.max_total_width = 700
        self.min_total_height = 20
        self.max_total_height = 100
        self.margin = 5

    def detect_rectangles(self,image_path):
        # Leer la imagen de entrada
        src = cv.imread(image_path)

        # Convertir la imagen a escala de grises y aplicar desenfoque
        src_gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
        src_gray = cv.blur(src_gray, (3, 3))

        # Procesar la imagen
        canny_output = cv.Canny(src_gray, self.threshold, self.threshold * 2)
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
        rectangles = sorted(rectangles, key=lambda r: (r[1], r[0]))  # Ordenar los rectángulos por coordenada Y y X

        merged_rectangles = []
        current_line = []
        prev_y = None
        prev_x = None

        for rect in rectangles:
            x, y, w, h = rect

            if prev_y is None or y - prev_y > self.max_line_gap:
                if current_line:
                    merged_rectangles.extend(self.merge_line_rectangles(current_line))
                    current_line = []

            if prev_x is not None and x - prev_x > self.max_char_gap:
                if current_line:
                    merged_rectangles.extend(self.merge_line_rectangles(current_line))
                    current_line = []

            current_line.append(rect)
            prev_y = y
            prev_x = x

        if current_line:
            merged_rectangles.extend(self.merge_line_rectangles(current_line))

        return merged_rectangles

    def merge_line_rectangles(self, rectangles):
        merged_rectangles = []

        line_rect = None
        line_min_x = float('inf')
        line_max_x = 0

        for rect in rectangles:
            x, y, w, h = rect

            if x < line_min_x:
                line_min_x = x

            if x + w > line_max_x:
                line_max_x = x + w

            if line_rect is None:
                line_rect = rect
            else:
                line_rect = (line_min_x, y, line_max_x - line_min_x, h)

        merged_rectangles.append(line_rect)

        return merged_rectangles


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