from PIL import Image
import numpy as np
import cv2
from scipy.ndimage import map_coordinates, gaussian_filter

def add_noise(image):
    # Convertir la imagen a un arreglo de NumPy
    image_array = np.array(image)
    # Generar ruido aleatorio
    noise = np.random.normal(0, 10, image_array.shape)
    # Sumar el ruido a la imagen
    noisy_image_array = image_array + noise
    # Asegurarse de que los valores estén en el rango correcto
    noisy_image_array = np.clip(noisy_image_array, 0, 255).astype(np.uint8)
    # Convertir el arreglo de vuelta a una imagen con Pillow
    noisy_image = Image.fromarray(noisy_image_array)

    return noisy_image

def elastic_transform(image, alpha, sigma):
    # Convertir la imagen a un arreglo de NumPy
    image_array = np.array(image)

    # Generar desplazamientos elásticos aleatorios
    random_state = np.random.RandomState(None)
    shape = image_array.shape
    dx = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma) * alpha
    dy = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma) * alpha

    # Crear mallas de coordenadas
    x, y = np.meshgrid(np.arange(shape[1]), np.arange(shape[0]))
    indices = x + dx, y + dy

    # Aplicar transformación elástica a la imagen
    transformed_image = map_coordinates(image_array, indices, order=1, mode='reflect')

    # Redimensionar la imagen transformada
    transformed_image = transformed_image.reshape(image_array.shape)

    # Convertir el arreglo de vuelta a una imagen con Pillow
    transformed_image = Image.fromarray(transformed_image.astype(np.uint8))

    return transformed_image


def perspective_transform(image, distortion):
    # Convertir la imagen a un arreglo de NumPy
    image_array = np.array(image)

    # Generar distorsiones perspectivas aleatorias con OpenCV
    width, height = image_array.shape[1], image_array.shape[0]
    distort = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32)
    d = distortion * np.random.rand(4, 2)
    distort += d
    matrix = cv2.getPerspectiveTransform(distort, np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32))

    # Aplicar distorsión perspectiva a la imagen con OpenCV
    transformed_image = cv2.warpPerspective(image_array, matrix, (width, height))

    # Convertir el arreglo de vuelta a una imagen con Pillow
    transformed_image = Image.fromarray(transformed_image)

    return transformed_image


# Cargar la imagen TIFF con PIL
image = Image.open('/home/jpmanzano/ocr-project/tesstrain/data/ocrafast-ground-truth/ocrafast_0.tif').convert('L')

# Aplicar ruido aleatorio a la imagen
noisy_image = add_noise(image)
elastic_image = elastic_transform(image, alpha=1000, sigma=10)
perspective_image = perspective_transform(image, distortion=100)


noisy_image_cv = np.array(noisy_image)
elastic_image_cv = np.array(elastic_image)
perspective_image_cv = np.array(perspective_image)

# Mostrar las imágenes en ventanas separadas utilizando OpenCV
cv2.imshow('Imagen con Ruido Aleatorio', noisy_image_cv)
cv2.imshow('Imagen con Def. Elástica', elastic_image_cv)
cv2.imshow('Imagen con Def. Perspectiva', perspective_image_cv)
cv2.waitKey(0)
cv2.destroyAllWindows()