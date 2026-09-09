### Histogramas, Umbralización y Detección de Bordes

La detección de bordes y la segmentación por umbralización son pilares fundamentales para aislar objetos en visión por computadora. Un **histograma de imagen** muestra la distribución de las intensidades de brillo de los píxeles.

### Histogramas e Igualación de Histograma

La igualación de histograma mejora el contraste de imágenes con bajo rango dinámico:

```python
import cv2
import matplotlib.pyplot as plt

imagen_gris = cv2.imread("imagen_oscura.jpg", cv2.IMREAD_GRAYSCALE)

# 1. Calcular el histograma con OpenCV (Imagen, Canales, Máscara, Tamaños bins, Rango)
hist = cv2.calcHist([imagen_gris], [0], None, [256], [0, 256])

# 2. Igualación de Histograma para mejorar el contraste global
imagen_igualada = cv2.equalizeHist(imagen_gris)
```

### Umbralización Binarizada (Thresholding) y Método de Otsu

La umbralización convierte una imagen en escala de grises en una imagen binaria (blanco y negro):

```python
import cv2

imagen_gris = cv2.imread("documento.jpg", cv2.IMREAD_GRAYSCALE)

# Umbralización simple (Valor umbral fijo = 127)
_, thresh_simple = cv2.threshold(imagen_gris, 127, 255, cv2.THRESH_BINARY)

# Umbralización Automática por Método de Otsu (calcula el umbral óptimo automáticamente)
_, thresh_otsu = cv2.threshold(imagen_gris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
```

### Detección de Bordes: Sobel y Canny

- **Filtro Sobel:** Calcula las derivadas espaciales de la imagen en las direcciones horizontal ($X$) y vertical ($Y$).
- **Algoritmo Canny:** El detector de bordes multietapa más popular (suavizado gaussiano, gradiente de intensidad, supresión de no máximos y umbralización con histéresis).

```python
import cv2

imagen_blur = cv2.GaussianBlur(imagen_gris, (5, 5), 0)

# Detección de bordes con Sobel
sobelx = cv2.Sobel(imagen_blur, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(imagen_blur, cv2.CV_64F, 0, 1, ksize=3)

# Detección de bordes Canny (Umbral inferior = 50, Umbral superior = 150)
bordes_canny = cv2.Canny(imagen_blur, threshold1=50, threshold2=150)
```

> **Consejo Práctico:** Antes de aplicar el detector de bordes `Canny`, aplica siempre un filtro `GaussianBlur` suave para reducir el ruido que podría generar falsos bordes.
