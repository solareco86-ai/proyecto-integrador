### Lectura, Escritura y Manipulación de Espacios de Color con OpenCV

En visión por computadora, una imagen digital se representa como una matriz numérico-espacial (matriz NumPy) de valores de píxeles. La librería `OpenCV` (`cv2`) lee por defecto las imágenes en formato **BGR** (Blue, Green, Red), a diferencia de la mayoría de librerías como Matplotlib o Pillow que utilizan **RGB**.

### Cargar y Guardar Imágenes (`cv2.imread` y `cv2.imwrite`)

Para cargar una imagen desde el disco y convertirla entre formatos de color:

```python
import cv2

# Cargar imagen en color (BGR)
imagen = cv2.imread("entrada.jpg")

# Verificar las dimensiones de la imagen (Alto, Ancho, Canales)
alto, ancho, canales = imagen.shape
print(f"Dimensiones: {ancho}x{alto}px - Canales: {canales}")

# Convertir de BGR a RGB para visualizar correctamente en Matplotlib
imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

# Convertir la imagen a escala de grises
imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# Guardar la imagen procesada en disco
cv2.imwrite("salida_grises.jpg", imagen_gris)
```

### Acceso a Píxeles y Canales Individuales

Al ser arreglos de `NumPy`, podemos separar y analizar los canales de color individualmente:

```python
import cv2

imagen = cv2.imread("entrada.jpg")

# Descomponer la imagen BGR en sus tres canales independientes
b, g, r = cv2.split(imagen)

# O bien mediante indexación directa de NumPy (más eficiente)
canal_azul = imagen[:, :, 0]
canal_verde = imagen[:, :, 1]
canal_rojo = imagen[:, :, 2]

# Recombinar canales modificados
imagen_recombinada = cv2.merge([b, g, r])
```

> **Consejo Práctico:** Al trabajar con OpenCV y Matplotlib en notebooks Jupyter, recuerda siempre usar `cv2.cvtColor(img, cv2.COLOR_BGR2RGB)` antes de llamar a `plt.imshow()`, de lo contrario las tonalidades azules y rojas aparecerán invertidas.
