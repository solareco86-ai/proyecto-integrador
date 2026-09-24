### Conversión de Espacios de Color con `cv2.cvtColor()` y Acceso a Canales

### ¿Qué hace `cv2.cvtColor()`?

`cv2.cvtColor()` es la función de OpenCV para **convertir una imagen de un espacio de color a otro**. Recibe la imagen de origen y un código de conversión (una constante que indica el espacio de color de entrada y el de salida), y devuelve un nuevo `numpy.ndarray` con los valores de píxel recalculados matemáticamente para el nuevo espacio — no es solo un "reetiquetado", los valores numéricos cambian.

```python
cv2.cvtColor(src, code)
```

* `src`: la imagen de origen (`numpy.ndarray`).
* `code`: constante de OpenCV que define la conversión, por ejemplo:
  * `cv2.COLOR_BGR2RGB`: reordena los canales, sin cambiar sus valores (solo invierte el orden B↔R).
  * `cv2.COLOR_BGR2GRAY`: promedia ponderadamente los tres canales de color en un único canal de intensidad (luminancia), reduciendo la imagen de 3 canales a 1.
  * `cv2.COLOR_BGR2HSV`: recalcula los valores a Matiz (*Hue*), Saturación y Valor, útil para segmentar por color de forma más robusta que en BGR/RGB.

```python
import cv2

imagen = cv2.imread("entrada.jpg")

# Convertir de BGR a RGB para visualizar correctamente en Matplotlib
imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

# Convertir la imagen a escala de grises (3 canales -> 1 canal)
imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
print(imagen.shape)       # (alto, ancho, 3)
print(imagen_gris.shape)  # (alto, ancho)  -> ya no tiene el eje de canales

# Guardar la imagen procesada en disco
cv2.imwrite("salida_grises.jpg", imagen_gris)
```

> **Consejo Práctico:** Al trabajar con OpenCV y Matplotlib en notebooks Jupyter, recuerda siempre usar `cv2.cvtColor(img, cv2.COLOR_BGR2RGB)` antes de llamar a `plt.imshow()`, de lo contrario las tonalidades azules y rojas aparecerán invertidas, ya que Matplotlib espera RGB y OpenCV entrega BGR.

### Acceso a Píxeles y Canales Individuales

Al ser arreglos de NumPy, podemos separar y analizar los canales de color individualmente sin pasar por `cvtColor`:

```python
import cv2

imagen = cv2.imread("entrada.jpg")

# Descomponer la imagen BGR en sus tres canales independientes
b, g, r = cv2.split(imagen)

# O bien mediante indexación directa de NumPy (más eficiente que cv2.split)
canal_azul = imagen[:, :, 0]
canal_verde = imagen[:, :, 1]
canal_rojo = imagen[:, :, 2]

# Recombinar canales modificados
imagen_recombinada = cv2.merge([b, g, r])
```

`cv2.split()` es más legible pero copia los datos en memoria por cada canal; la indexación directa (`imagen[:, :, n]`) es una vista sobre el mismo arreglo y resulta más eficiente cuando se procesan imágenes grandes o en lote.
