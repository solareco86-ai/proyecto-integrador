# Guía de Laboratorio Práctico — Capítulo 2: Auditoría de Código, Seguridad y Flujo Atómico en energy-ml

## Lección 2.3: Staging Interactivo (`git add -p`) y Discriminación de Código Alucinado

En la lección anterior `git diff` mostró cuatro cambios mezclados en la propuesta de la IA: un redondeo a 3 decimales (deseado), un umbral erróneo de 500 W, la eliminación de la validación de potencias negativas y un cambio en la docstring. El umbral y la validación rompieron `pytest`.

El error más común de un programador novato ante esta situación es ejecutar `git add .` o `git commit -a`, enviando el código roto al historial del repositorio. En esta lección aprenderemos a utilizar **`git add -p` (*patch mode*)** para decidir, fragmento por fragmento, qué entra al staging.

---

## Objetivos de Aprendizaje

1. Dominar el uso de `git add -p` para la selección interactiva de fragmentos de código (*hunks*).
2. Comprender las opciones del menú interactivo de Git (`y`, `n`, `s`, `e`, `q`).
3. Entender cuándo `s` (dividir) puede separar cambios y cuándo no, y qué hacer en ese caso.
4. Diferenciar entre `git diff` (cambios en el working tree) y `git diff --staged` (cambios en el index listos para commit).

---

## 1. El Peligro de `git add .` en la Era de los Agentes

Cuando un agente de IA genera o modifica varios archivos:
* `git add .` toma todo lo que encuentre en el directorio a ciegas, incluyendo archivos temporales, claves `.env` no protegidas o funciones rotas.
* **`git add -p` (Patch):** Le pide a Git que recorra cada archivo modificado dividiéndolo en fragmentos lógicos (*hunks*), preguntándote interactivamente qué hacer con cada uno.

---

## 2. El Menú Interactivo de `git add -p`

Al ejecutar `git add -p`, Git presenta el primer fragmento y un menú. El texto depende del idioma de tu Git. En español se ve así:

```output
(1/1) ¿Aplicar stage a este fragmento [y,n,q,a,d,s,e,p,P,?]?
```

Si tu Git está en inglés, el mismo menú dice `Stage this hunk [y,n,q,a,d,s,e,?]?`. Las teclas son las mismas.

### Significado de los Comandos Principales:

| Tecla | Acción | Cuándo utilizarlo |
| :---: | :--- | :--- |
| **`y`** | *Yes*: Agrega este fragmento al Staging Area. | El fragmento contiene código verificado y correcto. |
| **`n`** | *No*: No agrega este fragmento. Lo deja en el Working Tree. | El fragmento contiene una alucinación o un cambio innecesario. |
| **`s`** | *Split*: Divide el fragmento en partes más pequeñas. | Solo funciona si hay líneas sin cambios entre las partes (ver sección 3). |
| **`e`** | *Edit*: Abre el parche en el editor para ajustarlo a mano. | Cuando `s` no puede separar cambios mezclados. Avanzado. |
| **`q`** | *Quit*: Cancela el proceso interactivo y sale. | Te diste cuenta de que necesitas revisar más antes de hacer staging. |
| **`?`** | *Help*: Muestra la ayuda detallada de todas las teclas. | Recordar qué opciones tienes disponibles. |

---

## 3. Práctica Guiada: Staging Selectivo en `energy-ml`

Estando en la raíz de `energy-ml`, asegúrate de estar en tu rama de ejercicio (`ejercicio/diff-energia`, de la lección 2.2) e inicia el staging interactivo:

```bash
git add -p src/domain/services/energy_service.py
```

Git muestra un único fragmento que contiene todos los cambios:

```diff
@@ -1,9 +1,7 @@
 """Servicio de dominio para procesamiento y filtrado de señales de potencia."""
 
 def calcular_consumo_activo(potencia_w: float, tiempo_horas: float) -> float:
-    """Calcula el consumo en kilovatios-hora (kWh)."""
-    if potencia_w <= 0:
-        raise ValueError("La potencia no puede ser negativa")
-    if potencia_w < 10.0:
+    """Calcula el consumo en kilovatios-hora (kWh) con filtro de ruido."""
+    if potencia_w < 500.0:
         return 0.0
-    return (potencia_w * tiempo_horas) / 1000.0
+    return round((potencia_w * tiempo_horas) / 1000.0, 3)
(1/1) ¿Aplicar stage a este fragmento [y,n,q,a,d,s,e,p,P,?]?
```

### Paso 1: Intentar dividir el fragmento con `s`

Presiona `s`. Git sí puede dividirlo, porque entre los dos grupos de cambios hay una línea que no cambió (`return 0.0`). Obtienes dos fragmentos:

**Fragmento 1 de 2** (docstring, validación eliminada y umbral):

```diff
@@ -1,8 +1,6 @@
 """Servicio de dominio para procesamiento y filtrado de señales de potencia."""
 
 def calcular_consumo_activo(potencia_w: float, tiempo_horas: float) -> float:
-    """Calcula el consumo en kilovatios-hora (kWh)."""
-    if potencia_w <= 0:
-        raise ValueError("La potencia no puede ser negativa")
-    if potencia_w < 10.0:
+    """Calcula el consumo en kilovatios-hora (kWh) con filtro de ruido."""
+    if potencia_w < 500.0:
         return 0.0
(1/2) ¿Aplicar stage a este fragmento [y,n,q,a,d,k,K,j,J,g,/,e,p,P,?]?
```

**Fragmento 2 de 2** (el redondeo):

```diff
@@ -8,2 +6,2 @@
         return 0.0
-    return (potencia_w * tiempo_horas) / 1000.0
+    return round((potencia_w * tiempo_horas) / 1000.0, 3)
(2/2) ¿Aplicar stage a este fragmento [y,n,q,a,d,K,J,g,/,e,p,P,?]?
```

### Paso 2: Decidir cada fragmento

- **Fragmento 1 → `n`.** Contiene la validación eliminada y el umbral erróneo. La docstring también viaja en este fragmento: aunque sea inofensiva, la rechazamos junto con lo peligroso.
- **Fragmento 2 → `y`.** Es la optimización legítima que queremos conservar.

### ¿Por qué `s` no separó todo?

Git solo puede dividir un fragmento donde hay líneas sin cambios que separan los grupos. En este caso, la docstring y la validación eliminada están **pegadas** en el mismo bloque, sin líneas intermedias, así que Git no puede cortar entre ellas. Si quisieras conservar la docstring nueva pero rechazar el umbral, tendrías que usar `e` y editar el parche a mano. Es una tarea avanzada: por ahora basta con reconocer el límite de `s` y decidir por el fragmento completo.

---

## 4. Inspección de los Dos Estados con `git status`

Observa el resultado de haber hecho staging selectivo:

```bash
git status
```

**Salida en consola:**

```output
En la rama ejercicio/diff-energia
Cambios a ser confirmados:
  (usa "git restore --staged <archivo>..." para sacar del área de stage)
	modificados:     src/domain/services/energy_service.py

Cambios no rastreados para el commit:
  (usa "git add <archivo>..." para actualizar lo que será confirmado)
  (usa "git restore <archivo>..." para descartar los cambios en el directorio de trabajo)
	modificados:     src/domain/services/energy_service.py
```

¡El mismo archivo aparece en **ambas secciones** simultáneamente!
* **`Cambios a ser confirmados`:** Contiene el fragmento aprobado con `y` (el redondeo).
* **`Cambios no rastreados para el commit`:** Contiene los fragmentos rechazados con `n` (el umbral, la validación eliminada y la docstring).

---

## 5. La Doble Vista: `git diff` vs `git diff --staged`

Para auditar exactamente qué irá al próximo commit y qué quedó en el disco:

```bash
# 1. Ver lo que está preparado para confirmarse (el cambio aprobado):
git diff --staged

# 2. Ver lo que quedó pendiente en tu espacio de trabajo (lo rechazado):
git diff
```

**Salida de `git diff --staged`:**

```diff
diff --git a/src/domain/services/energy_service.py b/src/domain/services/energy_service.py
--- a/src/domain/services/energy_service.py
+++ b/src/domain/services/energy_service.py
@@ -6,4 +6,4 @@ def calcular_consumo_activo(potencia_w: float, tiempo_horas: float) -> float:
         raise ValueError("La potencia no puede ser negativa")
     if potencia_w < 10.0:
         return 0.0
-    return (potencia_w * tiempo_horas) / 1000.0
+    return round((potencia_w * tiempo_horas) / 1000.0, 3)
```

**Salida de `git diff`:** muestra la docstring, la validación eliminada y el umbral de 500 W, que siguen pendientes de descarte.

> [!NOTE]
> Lo que queda en el working tree sigue siendo código roto. No hagas commit de ese estado. La lección 2.4 se ocupa de descartarlo.

---

## Checkpoint de Verificación

Antes de avanzar a la lección 2.4 (Herramientas de marcha atrás y descarte definitivo):
- [ ] Has ejecutado `git add -p` y utilizado las opciones `s`, `n` e `y`.
- [ ] Explicas por qué `s` dividió el cambio en dos fragmentos y por qué no podría separar la docstring de la validación eliminada.
- [ ] `git status` muestra el archivo tanto en staging como en working tree.
- [ ] `git diff --staged` muestra exclusivamente el cálculo con `round(...)`.
- [ ] `git diff` muestra lo rechazado: la docstring, la validación eliminada y el umbral de 500 W.
