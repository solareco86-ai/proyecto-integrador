# 2.1 Filtros espaciales, suavizado y convolución

## ¿Qué es un filtro espacial y cómo funciona la convolución?
En el procesamiento digital de imágenes, un **filtro espacial** modifica el valor de cada píxel a partir de los valores de los píxeles vecinos dentro de una ventana o **vecindario** (por ejemplo, de $3 \times 3$ o $5 \times 5$).

La operación base es la **convolución** (o correlación espacial): se desliza un **kernel** (o máscara/filtro) sobre la imagen, se multiplican los pesos del kernel por los valores de los píxeles superpuestos y se suman los resultados para obtener el nuevo valor del píxel central.

* **Kernel de suavizado (promedio / promediado):** todos los pesos son positivos y suman $1$ (por ejemplo, $\frac{1}{9}$ en una ventana de $3 \times 3$). Atenúa variaciones bruscas entre píxeles vecinos y reduce ruido, pero también **difumina bordes y detalles finos**.
* **Tamaño del kernel:** un kernel más grande promedia más vecinos (más suavizado, mayor pérdida de nitidez y mayor costo de cómputo); un kernel más chico conserva más detalle local.
* **Bordes de la imagen:** al llegar a los bordes, la ventana supera los límites de la matriz. Suele resolverse mediante relleno (ceros, replicación del borde o reflexión).

### Implementación en OpenCV: Convolución y Filtro Promedio

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

## Ejemplo resuelto: ruido sal y pimienta con filtro de mediana
El **ruido sal y pimienta** aparece como píxeles aislados con valores extremos (blancos puros = "sal", negros puros = "pimienta") distribuidos de forma aleatoria.

* **Por qué falla el filtro promedio:** si un píxel de "sal" (255) cae dentro de un promedio de $3 \times 3$, arrastra hacia arriba el valor de todo el vecindario y deja una mancha grisácea borrosa.
* **Por qué funciona el filtro de mediana:** en lugar de promediar, ordena los valores de la ventana y toma el **valor central (mediana)**. Los valores extremos aislados quedan en los extremos de la lista ordenada y no dominan el resultado, limpiando el ruido impulsivo y preservando mucho mejor los bordes.

### Implementación en OpenCV: Filtro Gaussiano y Filtro de Mediana

```python
import cv2

imagen = cv2.imread("ruido_sal_pimienta.jpg")

# Filtro Gaussiano (Kernel de 5x5, sigmaX=0)
gaussiano = cv2.GaussianBlur(imagen, (5, 5), 0)

# Filtro Mediana (Kernel impar de 5)
mediana = cv2.medianBlur(imagen, 5)
```

> **Regla de Oro:** El tamaño del kernel en los filtros de convolución espacial casi siempre debe ser un número impar (3x3, 5x5, 7x7) para garantizar la existencia de un píxel central bien definido.

### Antes y después (ejemplo de referencia)
* **Original:** `static/img/cap_2_1/01_original.png`
* **Con ruido sal y pimienta:** `static/img/cap_2_1/04_ruido_sal_pimienta.png`
* **Resultado con filtro promedio (3x3):** `static/img/cap_2_1/05_sal_pimienta_con_promedio.png`
* **Resultado con filtro de mediana (3x3):** `static/img/cap_2_1/06_sal_pimienta_con_mediana.png`

## Ejercicio práctico: comparar filtros
1. Ejecutá `python3 scripts/demo_filtros_espaciales.py` y observá `02_suavizado_box_3x3.png` frente a `03_suavizado_box_9x9.png`. Anotá qué ocurre con los bordes de las figuras y la línea inferior.
2. Compará `05_sal_pimienta_con_promedio.png` y `06_sal_pimienta_con_mediana.png` sobre una imagen con ruido sal y pimienta.
3. **Pregunta de análisis para responder:** ¿En qué situación elegirías un filtro de mediana frente a un filtro promedio, y qué desventaja puede aparecer si subís demasiado el tamaño de la ventana?
