### Transformaciones Geométricas y Manipulación de Píxeles

Las transformaciones geométricas permiten alterar las dimensiones, orientación o perspectiva de las imágenes. En OpenCV, estas operaciones se realizan mapeando las coordenadas de la matriz original a una nueva matriz proyectada.

### Redimensionado (`cv2.resize`) y Recorte (Slicing de NumPy)

```python
import cv2

imagen = cv2.imread("entrada.jpg")

# 1. Redimensionar especificando dimensiones exactas (Ancho, Alto)
imagen_resized = cv2.resize(imagen, (640, 480), interpolation=cv2.INTER_AREA)

# 2. Redimensionar por factor de escala (ej. 50% del tamaño)
imagen_scaled = cv2.resize(imagen, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)

# 3. Recorte espacial (Crop) utilizando Slicing de NumPy: img[y_min:y_max, x_min:x_max]
recorte = imagen[100:300, 150:400]
```

### Rotación y Traslación con Matrices Afines

Para rotar una imagen alrededor de un punto central sin perder bordes:

```python
import cv2

imagen = cv2.imread("entrada.jpg")
(alto, ancho) = imagen.shape[:2]
centro = (ancho // 2, alto // 2)

# Obtener la matriz de rotación de 2x3 (Centro, Ángulo en grados, Escala)
matriz_rotacion = cv2.getRotationMatrix2D(centro, 45, 1.0)

# Aplicar la transformación afín a la imagen
imagen_rotada = cv2.warpAffine(imagen, matriz_rotacion, (ancho, alto))
```

> **Buenas Prácticas de Interpolación:** Utiliza `cv2.INTER_AREA` al reducir el tamaño de una imagen para evitar artefactos de aliasing, y `cv2.INTER_CUBIC` o `cv2.INTER_LINEAR` al ampliar dimensiones.
