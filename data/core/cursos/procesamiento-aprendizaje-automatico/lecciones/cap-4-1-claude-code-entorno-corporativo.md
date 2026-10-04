# Guía de Laboratorio — Lección 4.1: Claude Code (Opcional): El Estándar Corporativo y Gestión de Límites de Cuota

**Asignatura:** Nivel 0 — Procesamiento y Aprendizaje Automático Inicial  
**Capítulo 4:** Ecosistema Avanzado de IA Agéntica: Claude Code, Aider y Arneses Autónomos  
**Carga horaria estimada:** 25 min  
**Prerrequisitos:** Haber completado el Capítulo 3 (OpenCode y Antigravity CLI).

---

## 1. ¿Por Qué Claude Code es la Referencia en Empresas Tecnológicas?

En el sector empresarial, las compañías de software y los laboratorios de datos exigen herramientas con un nivel extremo de precisión analítica. En ese segmento, **Claude Code** (desarrollado por Anthropic) se ha consolidado como el estándar predilecto por tres motivos clave:

1. **Razonamiento de Frontera para Refactorizaciones Complejas:** La familia de modelos Claude (Claude 3.5 Sonnet y Claude 3.7 Sonnet) sobresale en la detección de sutilezas arquitectónicas, resolución de condiciones de carrera (*race conditions*) y respeto estricto de principios de diseño (SOLID, Clean Architecture).
2. **Naturaleza Git-Centric Nativa:** Opera directamente como un agente CLI que inspecciona git diffs, ejecuta comandos de terminal con control de permisos y formula parches quirúrgicos.
3. **Mecanismos de Seguridad y Gobernanza:** Exige autorización explícita antes de tocar archivos críticos o ejecutar comandos del sistema que puedan tener efectos secundarios destructivos.

> ℹ️ **Carácter Opcional en el ISFT N° 199:**  
> Esta lección está orientada a **estudiantes que ya se encuentran insertos en el mercado laboral** o cuyos empleadores les proporcionan licencias corporativas. No es obligatoria ni restrictiva para la aprobación académica del trayecto.

---

## 2. El Desafío Comercial: La Cuota Acotada de la Suscripción de 20 USD

Mientras que en Antigravity CLI los estudiantes disfrutan de una cuota muy amplia por 5 USD, la suscripción estándar de **Claude Pro / Team (20 USD/mes)** impone ventanas de control de velocidad (*rate limits*) dinámicas:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   DINÁMICA DE CUOTA EN CLAUDE CODE                     │
├────────────────────────────────────────────────────────────────────────┤
│ • Suscripción mensual fija: 20 USD por usuario.                       │
│ • Ventana de Recarga: Cuota dinámica evaluada cada 5 horas.           │
│ • Riesgo Agéntico: Un agente CLI lee árboles de archivos completos;   │
│   si no se poda el contexto, 4 o 5 consultas extensas pueden consumir  │
│   el 100% del cupo asignado para ese bloque de 5 horas.                │
└────────────────────────────────────────────────────────────────────────┘
```

Por lo tanto, operar con Claude Code requiere una disciplina de ahorro de contexto superior a cualquier otra herramienta.

---

## 3. Instalación y Autenticación Corporativa

Claude Code se instala a través del registro global de npm:

```bash
npm install -g @anthropic-ai/claude-code
```

### Inicio de Sesión

Para autenticar tu suscripción corporativa, ejecuta:

```bash
claude
```

El asistente abrirá el navegador para autorizar la conexión y guardar el token en tu perfil de usuario.

---

## 4. Buenas Prácticas de Ingeniería para No Agotar la Cuota en Minutos

Para evitar agotar el cupo de 5 horas durante una sesión de pair programming, aplica estas tres directivas:

### Regla 1: Usar Obligatoriamente `.claudeignore`
Al igual que un `.gitignore`, este archivo le prohíbe al agente leer carpetas pesadas que consumen miles de tokens inútilmente:
```text
.venv/
__pycache__/
*.csv
data/raw/
node_modules/
```

### Regla 2: Formular Instrucciones Atómicas (One-Shot Task)
No utilices a Claude Code para explorar vagamente un repositorio. Entrega la instrucción con el archivo exacto:

> *"Lee exclusivamente `src/pipeline.py` y agrega la función `calcular_frecuencia_muestreo(timestamps: list[datetime]) -> float`. No leas el resto del repositorio ni ejecutes comandos hasta que yo lo autorice."*

### Regla 3: Absorber la Verificación en tu Propia CPU Local ($0 Tokens)
No le pidas a Claude que ejecute `pytest` una y otra vez mientras intentas arreglar un bug. Corre `pytest` tú mismo en la terminal Bash, copia las 2 líneas exactas del error (*traceback*) y entrégaselas de forma precisa.

---

## 5. Taller Demostrativo en `energy-ml`

Imaginemos una tarea de refactorización arquitectónica en `energy-ml`:

```bash
cd ~/proyectos_software/energy-ml
claude
```

### Instrucción de Refactor Modular

> *"En `src/modelo.py`, la clase `ModeloPredictorEnergia` tiene mezcladas la carga de configuración y el cálculo de inferencia. Separa la lógica de configuración en una dataclass inmutable `ConfiguracionModelo` en `src/config.py`. Aplica tipado estricto con Python 3.12 y no agregues dependencias externas."*

Claude Code formulará el plan de acción, solicitará tu confirmación para crear `src/config.py` y modificará `src/modelo.py` mediante un diff quirúrgico.

Una vez aprobado:

```bash
git status
git diff
pytest
```

Consolidamos el trabajo:

```bash
git add src/config.py src/modelo.py
git commit -m "refactor(modelo): desacoplar ConfiguracionModelo asistido por Claude Code"
```

---

## 6. Conclusión

Claude Code es una herramienta de clase mundial para entornos corporativos con presupuesto dedicado. Sin embargo, su cuota acotada enseña una lección invaluable: **la disciplina de contexto y el ahorro de tokens son virtudes profesionales indispensables**.

En la siguiente lección, exploraremos **Aider**, la herramienta que nos permitirá abrir la caja negra de la IA agéntica mediante la API hiper-competitiva de **DeepSeek**.
