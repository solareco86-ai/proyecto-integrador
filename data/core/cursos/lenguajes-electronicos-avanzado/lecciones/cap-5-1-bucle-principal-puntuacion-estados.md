### La capa de aplicación

La capa de aplicación **coordina** el dominio con los puertos: no tiene reglas del negocio, pero decide el ritmo del juego, lee la entrada del jugador y ordena dibujar. **No importa** pygame ni machine.

### El bucle principal (game loop)

El juego avanza repitiendo siempre los mismos pasos:

1. Leer la dirección del jugador (puerto de control).
2. Avanzar un paso del dominio (`Partida.paso`).
3. Dibujar el estado (puerto de renderizado).
4. Esperar el tiempo del fotograma.

```python
class MotorDeJuego:
    def __init__(self, partida, renderizador, controlador, ia, colisiones,
                 fps=10):
        self.partida = partida
        self.renderizador = renderizador
        self.controlador = controlador
        self.ia = ia
        self.colisiones = colisiones
        self.fotograma = 1.0 / fps

    def ejecutar(self):
        while True:
            if self.partida.estado != "JUGANDO":
                self._dibujar()
                self._esperar()
                continue

            # 1. Entrada del jugador
            direccion = self.controlador.leer_direccion()
            self.partida.pacman.solicitar_direccion(direccion)

            # 2. Paso del dominio
            self.partida.paso(self.ia, self.colisiones)

            # 3. Dibujar
            self._dibujar()

            # 4. Esperar el fotograma
            self._esperar()

    def _dibujar(self):
        r = self.renderizador
        r.limpiar()
        self._dibujar_laberinto(r)
        r.dibujar_pacman(self.partida.pacman.x, self.partida.pacman.y)
        for fantasma in self.partida.fantasmas:
            r.dibujar_fantasma(fantasma.x, fantasma.y, fantasma.color)
        r.dibujar_texto("Score: %d" % self.partida.puntaje, 0, 54)
        r.mostrar()

    def _esperar(self):
        import time
        time.sleep(self.fotograma)
```

### Puntuación y estados

- **Puntaje**: lo acumula el dominio (`Partida.paso` suma 10 por bolita).
- **Estados**: `JUGANDO`, `GAME_OVER`, `VICTORIA`. La aplicación los muestra pero **quién los decide es el dominio** (colisión o bolitas agotadas).

### Probar en la PC sin placa

La aplicación se arma con los adaptadores elegidos. En la PC (pygame):

```python
juego = MotorDeJuego(
    partida=partida,
    renderizador=RenderizadorPygame(800, 600),
    controlador=ControladorTeclado(),
    ia=IA_Fantasmas(),
    colisiones=Colisiones(),
)
juego.ejecutar()
```

En el ESP32 (OLED + pulsadores):

```python
juego = MotorDeJuego(
    partida=partida,
    renderizador=RenderizadorOled(128, 64),
    controlador=ControladorPulsadores(),
    ia=IA_Fantasmas(),
    colisiones=Colisiones(),
)
juego.ejecutar()
```

**El único código que cambia es la composición en la infraestructura.**

### Micro-desafío práctico

> ¿Por qué `MotorDeJuego` recibe `ia` y `colisiones` por constructor en lugar de importarlas? ¿Qué ventaja tiene para probar la aplicación?

### Resumen

- La capa de aplicación orquesta: entrada → dominio → renderizado → espera.
- No contiene reglas del juego; solo coordina puertos y dominio.
- El bucle principal es `while True:` con un paso por fotograma.
- El puntaje y los estados los decide el dominio.
- Cambiar de PC a ESP32 solo cambia los adaptadores inyectados.
