### Filtrado Espacial y Suavizado de Imágenes

El filtrado espacial se utiliza para suprimir el ruido de una imagen o para resaltar detalles como bordes y textura. Se logra deslizando una pequeña matriz (llamada **kernel** o máscara) sobre la imagen y calculando la suma ponderada de los píxeles vecinos (convolución 2D).

### Convolución 2D y Filtro Promedio (Blur)

El filtro más simple reemplaza cada píxel por el promedio de sus vecinos dentro del área del kernel:

```python
import cv2
import numpy as np

imagen = cv2.imread("ruido.jpg")

# 1. Filtro Promedio con kernel de 5x5
imagen_blur = cv2.blur(imagen, (5, 5))

# 2. Convolución 2D personalizada usando cv2.filter2D
kernel_personalizado = np.ones((5, 5), np.float32) / 25
imagen_convolucion = cv2.filter2D(imagen, -1, kernel_personalizado)
```

### Filtro Gaussiano y Filtro Mediana (Eliminación de Ruido)

- **Filtro Gaussiano (`cv2.GaussianBlur`):** Pondera más los píxeles centrales según una distribución normal. Ideal para ruido gaussiano.
- **Filtro Mediana (`cv2.medianBlur`):** Reemplaza cada píxel por la mediana de los píxeles del kernel. Extremadamente efectivo para eliminar ruido de tipo "sal y pimienta" preservando bordes nítidos.

```python
import cv2

imagen = cv2.imread("ruido_sal_pimienta.jpg")

# Filtro Gaussiano (Kernel de 5x5, sigmaX=0)
gaussiano = cv2.GaussianBlur(imagen, (5, 5), 0)

# Filtro Mediana (Kernel impar de 5)
mediana = cv2.medianBlur(imagen, 5)
```

> **Regla de Oro:** El tamaño del kernel en los filtros de convolución espacial casi siempre debe ser un número impar (3x3, 5x5, 7x7) para garantizar la existencia de un píxel central bien definido.
