# Guion: Histogramas, brillo y contraste (capítulo 2.2)

Video sin voz, de 1:29, con textos en pantalla y música de fondo generada por computadora. Lo arma `scripts/generar_video_histogramas_2_2.py` a partir de las imágenes de la lección 2.2, así que muestra exactamente los mismos resultados que el texto. Está publicado en la lección como `static/media/cursos/pdi/video-histogramas-brillo-contraste.mp4`.

## Escena 1: Portada (0:00 - 0:05)
Título, materia y lección.

## Escena 2: ¿Qué es un histograma? (0:05 - 0:17)
Retina real y su histograma, que se dibuja de izquierda a derecha.
- El histograma cuenta cuántos píxeles hay de cada tono de gris, del 0 (negro) al 255 (blanco).
- En esta retina casi todos los tonos están amontonados en el medio: por eso se ve apagada.

## Escena 3: Brillo (0:17 - 0:30)
El brillo sube y baja (de −75 a +75) y el histograma se mueve en vivo.
- Subir el brillo suma el mismo valor a todos los píxeles; bajarlo, lo resta.
- El histograma se corre entero hacia un lado, pero no cambia de forma: el contraste sigue igual.

## Escena 4: Contraste (0:30 - 0:44)
El contraste sube de ×1,0 a ×2,6 y vuelve.
- Subir el contraste multiplica la distancia de cada tono al medio.
- El histograma se estira. Si se estira de más, los tonos se amontonan en 0 y 255 y se pierde detalle.

## Escena 5: Ecualización (0:44 - 0:57)
Original contra ecualizada, con los dos histogramas.
- La ecualización reparte los tonos para que ocupen todo el rango.
- Los vasos se ven mucho más, pero el fondo negro se vuelve gris y la zona clara del nervio se quema.

## Escena 6: CLAHE (0:57 - 1:08)
Ecualización global contra CLAHE.
- CLAHE ecualiza por zonas y limita cuánto puede estirar el contraste.
- El fondo sigue negro y la zona del nervio conserva su detalle.

## Escena 7: Umbral de Otsu (1:08 - 1:21)
Monedas reales: una línea roja recorre el histograma hasta el 107 y la imagen se binariza en vivo.
- El histograma también sirve para separar los objetos del fondo.
- Otsu prueba los 256 umbrales y elige el que mejor separa los dos grupos de tonos: acá, 107.

## Escena 8: Resumen (1:21 - 1:29)
Brillo corre el histograma, contraste lo estira, la ecualización lo reparte, CLAHE lo reparte por zonas y Otsu lo corta en dos.
