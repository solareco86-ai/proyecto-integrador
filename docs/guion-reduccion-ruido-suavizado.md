# Guion: Reducción de ruido y suavizado en imágenes (Capítulo 2.1)

## Bloque 1: Introducción (0:00 - 0:30)
Hoy vemos cómo funcionan la reducción de ruido y el suavizado en el procesamiento digital de imágenes.
Cuando capturamos o procesamos una imagen, pueden aparecer variaciones no deseadas o ruido que dificultan su lectura o análisis.

## Bloque 2: Convolución y suavizado (0:30 - 1:10)
Un filtro espacial desliza una ventana o kernel sobre la imagen y calcula el valor de cada píxel a partir de sus vecinos.
Con un filtro promedio, cada píxel toma el promedio de su vecindario: esto suaviza fluctuaciones, pero al agrandar la ventana se pierde nitidez en los bordes.

## Bloque 3: Ruido sal y pimienta — Promedio vs. Mediana (1:10 - 2:00)
En una imagen con ruido sal y pimienta aparecen píxeles extremos blancos y negros repartidos al azar.
Un filtro promedio arrastra esos extremos y genera manchas borrosas; en cambio, el filtro de mediana ordena los valores del vecindario y toma el valor central, limpiando mejor el ruido impulsivo y conservando más los bordes.

## Bloque 4: Cierre (2:00 - 2:20)
Elegir el filtro adecuado depende del tipo de ruido y del equilibrio entre limpiar y conservar detalles. Podés probar y comparar estos resultados ejecutando el código del capítulo 2.1.
