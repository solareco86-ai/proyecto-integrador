# Guía de Laboratorio Práctico — Capítulo 2: Auditoría de Código y Flujo Atómico de Cambios

**Módulo:** Procesamiento y Aprendizaje Automático Inicial (Nivel 0 — Nivelación)  
**Slug:** `procesamiento-aprendizaje-automatico-inicial`  
**Carga del Capítulo:** 3 horas (de 20 hs totales)

---

## Objetivos de Aprendizaje

Al finalizar este laboratorio, el estudiante será capaz de:
1. Descartar selectivamente fragmentos de código inseguro o no deseado del working tree mediante `git restore -p` (o `git checkout -p`).
2. Validar la integridad y ejecución del script en Python tras la depuración.
3. Crear un commit atómico y semántico que documente con precisión el cambio validado.
4. Inspeccionar el historial de Git con `git log --oneline --graph`.
5. Aplicar la Rúbrica y Protocolo de Auditoría Anti-Aceptación Ciega para interactuar con agentes en el Capítulo 3.

---

## 1. Descarte Quirúrgico de Código Inseguro con `git restore -p`

En la lección anterior colocamos la función `calcular_desviacion_estandar` en staging (`git add -p`), dejando fuera la variable con la API key y el log invasivo. Sin embargo, esas líneas peligrosas todavía están escritas en el archivo `calculadora_datos.py` en tu disco.

Para eliminarlas sin tener que editar a mano ni correr el riesgo de borrar lógica válida, Git provee el descarte interactivo:

```bash
git restore -p calculadora_datos.py
# (En versiones más antiguas de Git, el equivalente es: git checkout -p calculadora_datos.py)
```

Git te presentará los fragmentos que **no** están en staging y te preguntará:

```text
Discard this hunk from worktree [y,n,q,a,d,e,?]?
```

### Instrucciones de Descarte:
1. Para el bloque que contiene la `API_KEY_TEMP`, presiona **`y`** (sí, descartar y eliminar del archivo).
2. Para el bloque con el `print` del log invasivo, presiona **`y`** (sí, descartar y eliminar del archivo).

Una vez completado, revisa el estado del repositorio:

```bash
git status
```

Verás que el working tree está completamente limpio:
```text
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   calculadora_datos.py
```

---

## 2. Verificación de Integridad en Terminal

Antes de registrar el commit, valida que el código es sintácticamente correcto y que no quedaron llamadas huérfanas:

```bash
python3 calculadora_datos.py
```

### Salida esperada:
```text
Datos: [10.5, 20.0, 30.2, 40.8]
Promedio: 25.38
Varianza: 172.95
Desviación Estándar: 13.15
```

Comprueba que la ejecución concluye de forma limpia, sin mostrar ningún log con claves secretas ni errores de ejecución.

---

## 3. Registro del Commit Atómico y Auditoría del Historial

Aplica el commit semántico siguiendo las mejores prácticas de la industria:

```bash
git commit -m "feat: agregar calculo de desviacion estandar validado"
```

Ahora inspecciona la genealogía completa del repositorio:

```bash
git log --oneline --graph --decorate
```

### Ejemplo de Salida:
```text
* 7f8a9b0 (HEAD -> main) feat: agregar calculo de desviacion estandar validado
* 3c2d1e0 feat: agregar calculo de varianza muestral
* 1a2b3c4 feat: version inicial de calculadora_datos y gitignore
```

Observa la belleza de un historial atómico: cada commit representa una unidad lógica funcional verificada, sin código alucinado, sin credenciales expuestas y sin mensajes ambiguos.

---

## 4. Protocolo de Auditoría y Rúbrica de Evaluación

Antes de conectar asistentes CLI en el Capítulo 3 (Aider, OpenCode y AGY CLI), adopta este protocolo de 5 puntos como norma profesional:

| Criterio | Pregunta de Control | Acción Requerida |
| :--- | :--- | :--- |
| **1. Necesidad del Cambio** | ¿El agente modificó archivos o líneas que no formaban parte de la instrucción? | Rechazar o revertir con `git restore`. |
| **2. Protección de Secretos** | ¿Hay claves, contraseñas o tokens embebidos en el código? | Extraerlos a variables de entorno (`.env`) e ignorar con `.gitignore`. |
| **3. Corrección Matemática/Lógica** | ¿Los cálculos y algoritmos respetan las fórmulas esperadas? | Verificar con tests o ejecuciones en consola. |
| **4. Granularidad (Staging)** | ¿Estamos mezclando dos funcionalidades distintas en un mismo commit? | Usar `git add -p` para separar en commits atómicos. |
| **5. Mensaje Convencional** | ¿El mensaje de commit describe con claridad el "qué" y el "por qué"? | Usar prefijos estándar: `feat:`, `fix:`, `refactor:`, `test:`. |

---

## Checkpoint de Auditoría del Capítulo 2

Antes de avanzar al **Capítulo 3 (La Tríada de Asistentes: Aider, OpenCode y AGY CLI)**, confirma:
- [ ] Has ejecutado `git restore -p` y verificado que `API_KEY_TEMP` fue erradicada de `calculadora_datos.py`.
- [ ] El script `python3 calculadora_datos.py` ejecuta y produce los valores estadísticos exactos.
- [ ] Tu historial de `git log --oneline` contiene únicamente commits atómicos y claros.
- [ ] Comprendes el flujo: **Propuesta de Agente $\to$ `git diff` $\to$ `git add -p` $\to$ `git restore -p` $\to$ `python script.py` $\to$ `git commit`**.
