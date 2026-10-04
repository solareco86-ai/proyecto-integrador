# Guía de Laboratorio Práctico — Capítulo 2: Auditoría de Código, Seguridad y Flujo Atómico en energy-ml

## Lección 2.3: Staging Interactivo (`git add -p`) y Discriminación de Código Alucinado

En la lección anterior utilizamos `git diff` para descubrir que la IA introdujo una mejora legítima (redondeo a 3 decimales) combinada con una alucinación destructiva (un umbral erróneo de 500W que rompió `pytest`).

El error más común de un programador novato ante esta situación es ejecutar `git add .` o `git commit -a`, enviando el código roto al historial del repositorio. En esta lección aprenderemos a utilizar **`git add -p` (*patch mode*)** para discriminar hunks quirúrgicamente: seleccionando sólo las partes seguras y dejando fuera las líneas defectuosas.

---

## Objetivos de Aprendizaje

1. Dominar el uso de `git add -p` para la selección interactiva de fragmentos de código (*hunks*).
2. Comprender las opciones del menú interactivo de Git (`y`, `n`, `s`, `e`, `q`).
3. Aprender a dividir (*split*) bloques mixtos para separar mejoras deseadas de alucinaciones.
4. Diferenciar entre `git diff` (cambios en el working tree) y `git diff --staged` (cambios en el index listos para commit).

---

## 1. El Peligro de `git add .` en la Era de los Agentes

Cuando un agente de IA genera o modifica varios archivos:
* `git add .` toma todo lo que encuentre en el directorio a ciegas, incluyendo archivos temporales, claves `.env` no protegidas o funciones rotas.
* **`git add -p` (Patch):** Le pide a Git que recorra cada archivo modificado dividiéndolo en fragmentos lógicos (*hunks*), preguntándote interactivamente qué hacer con cada uno.

---

## 2. El Menú Interactivo de `git add -p`

Al ejecutar `git add -p`, Git presenta el primer bloque de cambios y muestra el siguiente menú en la consola:

```output
Stage this hunk [y,n,q,a,d,s,e,?]? 
```

### Significado de los Comandos Principales:

| Tecla | Acción | Cuándo utilizarlo |
| :---: | :--- | :--- |
| **`y`** | *Yes*: Agrega este hunk al Staging Area. | El bloque contiene código 100% verificado y correcto. |
| **`n`** | *No*: No agrega este hunk. Lo deja en el Working Tree. | El bloque contiene una alucinación o cambio innecesario. |
| **`s`** | *Split*: Divide el hunk en partes más pequeñas. | El bloque mezcla una mejora legítima con una línea errónea. |
| **`e`** | *Edit*: Abre el editor para ajustar las líneas manualmente. | Quieres corregir un valor numérico directamente en el parche. |
| **`q`** | *Quit*: Cancela el proceso interactivo y sale. | Te diste cuenta de que necesitas revisar más antes de hacer staging. |
| **`?`** | *Help*: Muestra la ayuda detallada de todas las teclas. | Recordar qué opciones tienes disponibles. |

---

## 3. Práctica Guiada: Staging Selectivo en `energy-ml`

Estando en la raíz de `energy-ml`, inicia el staging interactivo:

```bash
git add -p src/domain/services/energy_service.py
```

Git te mostrará el bloque modificado en la lección anterior:

```diff
Stage this hunk [y,n,q,a,d,s,e,?]? 
```

### Paso 1: Dividir el bloque mixto con `s`
Como el bloque contiene tanto la mejora deseada (el redondeo) como la alucinación (el umbral de 500W), presiona:

```bash
s
```

Git dividirá el cambio en dos sub-bloques independientes:

1. **Sub-bloque 1 (El umbral erróneo):**
   ```diff
   @@ -4,3 +4,3 @@
   -    if potencia_w < 10.0:
   -        return 0.0
   +    if potencia_w < 500.0:
   +        return 0.0
   Stage this hunk [y,n,q,a,d,j,J,g,/,e,?]? 
   ```
   Como este es el umbral que rompió la prueba, presiona **`n`** (No incluir).

2. **Sub-bloque 2 (El cálculo con redondeo):**
   ```diff
   @@ -8,2 +8,2 @@
   -    return (potencia_w * tiempo_horas) / 1000.0
   +    return round((potencia_w * tiempo_horas) / 1000.0, 3)
   Stage this hunk [y,n,q,a,d,K,g,/,e,?]? 
   ```
   Esta es la optimización legítima y deseada. Presiona **`y`** (Sí incluir).

---

## 4. Inspección de los Dos Estados con `git status`

Observa el resultado de haber hecho staging selectivo:

```bash
git status
```

**Salida en consola:**

```output
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   src/domain/services/energy_service.py

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   src/domain/services/energy_service.py
```

¡El mismo archivo aparece en **ambas secciones** simultáneamente!
* **`Changes to be committed`:** Contiene las líneas aprobadas con `y` (el redondeo).
* **`Changes not staged for commit`:** Contiene las líneas rechazadas con `n` (el umbral de 500W).

---

## 5. La Doble Vista: `git diff` vs `git diff --staged`

Para auditar exactamente qué irá al próximo commit y qué quedó en el disco:

```bash
# 1. Ver lo que está preparado para confirmarse (el cambio aprobado):
git diff --staged

# 2. Ver lo que quedó pendiente en tu espacio de trabajo (la alucinación):
git diff
```

---

## Checkpoint de Verificación

Antes de avanzar a la lección 2.4 (Herramientas de marcha atrás y descarte definitivo):
- [ ] Has ejecutado `git add -p` y utilizado las opciones `s`, `n` e `y`.
- [ ] `git status` muestra el archivo tanto en staging como en working tree.
- [ ] `git diff --staged` muestra exclusivamente el cálculo con `round(...)`.
- [ ] `git diff` muestra exclusivamente el umbral de 500W pendiente de descarte.
