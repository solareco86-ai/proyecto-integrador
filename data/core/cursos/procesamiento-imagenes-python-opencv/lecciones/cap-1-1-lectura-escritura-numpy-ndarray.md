### Lectura y Escritura de Imágenes: el Objeto `numpy.ndarray`

En visión por computadora, una imagen digital se representa como una matriz numérico-espacial (matriz NumPy) de valores de píxeles. La librería `OpenCV` (`cv2`) lee por defecto las imágenes en formato **BGR** (Blue, Green, Red), a diferencia de la mayoría de librerías como Matplotlib o Pillow que utilizan **RGB**.

### Cargar y Guardar Imágenes (`cv2.imread` y `cv2.imwrite`)

Para cargar una imagen desde el disco:

```python
import cv2

# Cargar imagen en color (BGR)
imagen = cv2.imread("entrada.jpg")

# Verificar las dimensiones de la imagen (Alto, Ancho, Canales)
alto, ancho, canales = imagen.shape
print(f"Dimensiones: {ancho}x{alto}px - Canales: {canales}")

# Guardar la imagen en disco (por ejemplo, tras alguna modificación)
cv2.imwrite("salida.jpg", imagen)
```

### ¿Qué es realmente el objeto `imagen`?

En Python, **todo es un objeto**, y en este caso concreto `imagen` es una instancia de la clase **`numpy.ndarray`** (si el archivo se leyó correctamente).

OpenCV en Python no utiliza una clase propia llamada `Image`, sino que representa las imágenes como matrices multidimensionales de NumPy (*n-dimensional array*):

```python
import cv2

imagen = cv2.imread("entrada.jpg")

print(type(imagen))
# <class 'numpy.ndarray'>

print(isinstance(imagen, object))
# True
```

**Características del objeto `numpy.ndarray`:**

* **Atributos:**
  * `imagen.shape`: Devuelve una tupla con las dimensiones `(alto, ancho, canales)`. Por ejemplo, `(1080, 1920, 3)`.
  * `imagen.dtype`: Tipo de dato de los píxeles (habitualmente `uint8`, valores de 0 a 255).
  * `imagen.size`: Cantidad total de elementos (alto × ancho × canales).
  * `imagen.ndim`: Cantidad de dimensiones del arreglo (por ejemplo, 3 para una imagen en color, 2 para una imagen en escala de grises).
* **Métodos:** Al ser un `ndarray`, `imagen` permite realizar operaciones vectorizadas, rebanados (*slicing*), transformaciones matemáticas directas (suma, resta, multiplicación elemento a elemento) y manipulaciones de canales sin necesidad de recorrer píxel por píxel con bucles `for` — lo cual sería órdenes de magnitud más lento.

```python
# Cada píxel es un sub-arreglo de 3 valores (B, G, R) cuando la imagen tiene color
pixel = imagen[100, 200]
print(pixel)
# array([120,  85, 200], dtype=uint8)

# Modificar un píxel directamente (indexación estilo NumPy: [fila, columna])
imagen[100, 200] = [0, 0, 0]
```

> **Detalle a tener en cuenta:** Si la ruta es incorrecta o el archivo no existe, `cv2.imread()` no lanza un error, sino que devuelve `None` (que en Python también es un objeto, instancia de `NoneType`). Por eso es común verificar `if imagen is not None:` antes de procesarla.
