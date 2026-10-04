# Guía de Laboratorio — Lección 3.4: Claude Code (Opcional): El Estándar Corporativo y Gestión de Límites de Cuota

**Asignatura:** Nivel 0 — Procesamiento y Aprendizaje Automático Inicial  
**Capítulo 3:** El Cuarteto de IA Agéntica: OpenCode, Antigravity CLI, Claude Code y Aider  
**Carga horaria estimada:** 25 min  
**Prerrequisitos:** Haber completado la Lección 3.3 (Antigravity CLI).

---

## 1. ¿Por Qué Claude Code es la Referencia Corporativa?

En el sector empresarial y tecnológico, **Claude Code** (desarrollado por Anthropic) se ha consolidado como la herramienta preferida por líderes técnicos, arquitectos de software y equipos de ingeniería:

* **Razonamiento Arquitectónico Riguroso:** La familia de modelos Claude (Claude 3.5 Sonnet y Claude 3.7 Sonnet) destaca por su precisión en refactorizaciones a gran escala, detección de condiciones de carrera (*race conditions*) y comprensión de dependencias complejas.
* **Integración Nativa con el Sistema Operativo:** Diseñado específicamente como un agente CLI que inspecciona git diffs, ejecuta comandos de terminal de forma controlada y propone parches atómicos.
* **Auditoría de Seguridad y Permisos:** Incluye un esquema estricto de confirmación antes de ejecutar comandos destructivos o modificar archivos fuera del directorio de trabajo.

> ℹ️ **Carácter Opcional en el ISFT N° 199:**  
> Esta lección está orientada a **estudiantes que ya se encuentran insertos en el mercado laboral** o que cuentan con acceso a licencias provistas por sus empleadores. No es un requisito obligatorio ni excluyente para aprobar la materia.

---

## 2. El Desafío del Modelo Comercial: La Cuota Acotada de 20 USD

A diferencia de modelos con cuota holgada o API por consumo granular, la suscripción mensual de **Claude Pro / Team (20 USD/mes)** opera con una ventana de cuota estricta:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   DINÁMICA DE CUOTA EN CLAUDE CODE                     │
├────────────────────────────────────────────────────────────────────────┤
│ • Suscripción: 20 USD mensuales fijos por usuario.                     │
│ • Ventana de Recarga: Cuota dinámica evaluada cada 5 horas.           │
│ • Riesgo Agéntico: Un agente CLI lee árboles de archivos completos;   │
│   si no se poda el contexto, 4 o 5 consultas extensas pueden consumir  │
│   el 100% de la cuota disponible para ese bloque de 5 horas.           │
└────────────────────────────────────────────────────────────────────────┘
```

Por esta razón, utilizar Claude Code exige una **disciplina de contexto superior** a cualquier otra herramienta.

---

## 3. Instalación y Autenticación

Claude Code se distribuye a través del registro global de npm:

```bash
npm install -g @anthropic-ai/claude-code
```

### Inicio de Sesión Corporativa

Dentro de la terminal, inicia el asistente para autenticar tu cuenta:

```bash
claude
```

El asistente solicitará autorización vía navegador para enlazar la suscripción activa.

---

## 4. Estrategias de Conservación de Cuota en Proyectos Reales

Para evitar agotar el cupo de 5 horas en los primeros 15 minutos de desarrollo, sigue estas tres reglas de oro:

### Regla 1: Nunca Iniciar en la Raíz sin Restricciones
Si ejecutas `claude` en un repositorio con carpetas `node_modules/`, `.venv/` o datos masivos en `data/`, el agente consumirá decenas de miles de tokens solo para indexar:
* Configura siempre un archivo `.claudeignore` (equivalente a `.gitignore`) excluyendo carpetas pesadas:
  ```text
  .venv/
  __pycache__/
  data/raw/
  *.csv
  ```

### Regla 2: Formular Prompts Quirúrgicos (One-Shot Task)
En lugar de iniciar un diálogo exploratorio informal, entrega la instrucción completa con archivos delimitados:

> *"Lee únicamente `src/modelo.py` y agrega validación de dimensiones en la entrada `X`. No leas el resto del repositorio ni ejecutes tests hasta que yo lo autorice."*

### Regla 3: Delegar la Ejecución Pesada a la CPU Local
No uses a Claude para que "mire" cómo fallan los tests en un bucle interactivo. Ejecuta `pytest` en tu terminal local, copia únicamente las 3 líneas del traceback del fallo y entrégaselas de forma precisa.

---

## 5. Taller Demostrativo sobre `energy-ml`

Imaginemos un escenario de refactorización arquitectónica en `energy-ml`:

```bash
cd ~/proyectos_software/energy-ml
claude
```

### Instrucción de Refactorización Modular

> *"En `src/modelo.py`, la clase `ModeloPredictorEnergia` tiene acoplada la carga de configuración y el entrenamiento. Separa la lógica de configuración en una dataclass inmutable `ConfiguracionModelo` en `src/config.py`. Respeta tipado estricto con Python 3.12 y no agregues dependencias externas."*

### Auditoría del Diff Generado

Claude Code presentará el plan de acción, solicitará confirmación para crear `src/config.py` y modificará `src/modelo.py`. Una vez aceptado el parche:

```bash
git status
git diff
pytest tests/
```

Confirmamos el cambio en el control de versiones:

```bash
git add src/config.py src/modelo.py
git commit -m "refactor(modelo): desacoplar ConfiguracionModelo asistido por Claude Code"
```

---

## 6. Conclusión

Claude Code es un estándar de excelencia en la industria cuando se dispone del presupuesto corporativo. Sin embargo, su cuota acotada demuestra por qué **saber administrar el contexto y los tokens** es una habilidad profesional tan relevante como escribir código.

En la siguiente lección, exploraremos **Aider**, el agente que nos permitirá abrir la caja negra de la IA agéntica mediante la API ultra-económica de **DeepSeek**.
