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

### ¿Qué es realmente el objeto `imagen`?

En Python, **todo es un objeto**, y en este caso concreto `imagen` es una instancia de la clase **`numpy.ndarray`** (si el archivo se leyó correctamente).

OpenCV en Python no utiliza una clase propia llamada `Image`, sino que representa las imágenes como matrices multidimensionales de NumPy:

```python
import cv2

imagen = cv2.imread("entrada.jpg")

print(type(imagen))
# <class 'numpy.ndarray'>

print(isinstance(imagen, object))
# True
```

**Características del objeto `imagen`:**

* **Atributos:**
  * `imagen.shape`: Devuelve una tupla con las dimensiones `(alto, ancho, canales)`. Por ejemplo, `(1080, 1920, 3)`.
  * `imagen.dtype`: Tipo de dato de los píxeles (habitualmente `uint8`, valores de 0 a 255).
  * `imagen.size`: Cantidad total de elementos (alto × ancho × canales).
* **Métodos:** Permite realizar operaciones vectorizadas, rebanados (*slicing*), transformaciones matemáticas directas y manipulaciones de canales.

> **Detalle a tener en cuenta:** Si la ruta es incorrecta o el archivo no existe, `cv2.imread()` no lanza un error, sino que devuelve `None` (que en Python también es un objeto, instancia de `NoneType`). Por eso es común verificar `if imagen is not None:` antes de procesarla.
