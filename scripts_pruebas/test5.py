import cv2

def detectar_rectangulos(imagen):
    # Convertir la imagen a escala de grises
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Aplicar un umbral adaptativo a la imagen
    _, imagen_umbral = cv2.threshold(imagen_gris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # cv2.imshow('Rectángulos detectados', imagen_umbral)
    # cv2.waitKey(0)

    # El umbralizado esta perfecto, este no es el problema

    # Encontrar los contornos en la imagen
    contornos, _ = cv2.findContours(imagen_umbral, cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)

    # Filtrar los contornos que representan rectángulos
    rectangulos = []
    for contorno in contornos:
        perimetro = cv2.arcLength(contorno, True)
        aproximacion = cv2.approxPolyDP(contorno, 0.08 * perimetro, True)
        if len(aproximacion) == 4:
            rectangulos.append(aproximacion)

    # Dibujar los rectángulos en la imagen original
    imagen_con_rectangulos = imagen.copy()
    cv2.drawContours(imagen_con_rectangulos, rectangulos, -1, (0, 255, 0), 2)

    # Mostrar la imagen con los rectángulos detectados
    cv2.imshow('Rectángulos detectados', imagen_con_rectangulos)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Cargar la imagen en color (BGR)
imagen = cv2.imread('test/img2/20230615131504.bmp', cv2.IMREAD_COLOR)

# Detectar rectángulos en la imagen
detectar_rectangulos(imagen)
