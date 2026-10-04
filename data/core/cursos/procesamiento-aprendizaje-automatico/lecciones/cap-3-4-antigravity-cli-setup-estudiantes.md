# Guía de Laboratorio — Lección 3.4: Antigravity CLI: Tarifa Estudiantil de 5 USD/mes, Instalación y Atajos de Teclado

**Asignatura:** Nivel 0 — Procesamiento y Aprendizaje Automático Inicial  
**Capítulo 3:** Asistentes de IA para Estudiantes: OpenCode y Antigravity CLI  
**Carga horaria estimada:** 25 min  
**Prerrequisitos:** Haber completado la Lección 3.3 (Laboratorio con OpenCode).

---

## 1. El Salto a Modelos de Frontera con Presupuesto Estudiantil

Mientras que OpenCode nos brinda una base libre y gratuita invaluable, los proyectos complejos de Ciencia de Datos a menudo requieren modelos de razonamiento de frontera capaces de analizar cientos de líneas de código, generar planes de refactorización multi-etapa y navegar la web.

En el mercado comercial, suscripciones como ChatGPT Plus o Claude Pro cuestan 20 USD mensuales, un costo elevado para la realidad de muchos estudiantes en Argentina.

Aquí es donde **Antigravity CLI (`agy`)**, desarrollado por Google DeepMind, se posiciona como **la mejor relación calidad/precio del planeta**:
* **Descuento Estudiantil Oficial:** Acreditando tu condición de estudiante regular del ISFT N° 199 (mediante correo oficial `@abc.gob.ar` o constancia de alumno regular), accedes a un **descuento de 15 USD mensuales durante 12 meses consecutivos**.
* **Costo Real:** Pagas únicamente **5 USD por mes**.
* **Cuota de Uso Excepcionalmente Generosa:** Por 5 USD accedes a modelos Gemini Pro y Flash con capacidades de contexto masivo (hasta 1 millón de tokens) sin los bloqueos frecuentes por límite de mensajes que afectan a otras plataformas.

---

## 2. Instalación de Antigravity CLI en Linux

Abre tu terminal Bash y ejecuta el script instalador oficial:

```bash
curl -fsSL https://antigravity.google/install.sh | bash
```

El instalador colocará el binario compilado en `~/.local/bin/agy` o en `/usr/local/bin/agy` y actualizará tu variable de entorno `$PATH`.

### Verificación de Instalación

Reinicia tu terminal o recarga tu configuración:

```bash
source ~/.bashrc
agy --version
```

Deberás observar la versión de Antigravity CLI activa en tu sistema.

---

## 3. Autenticación con Beneficio Educativo

Para vincular tu cuenta estudiantil bonificada, ejecuta:

```bash
agy auth login
```

1. El comando abrirá una ventana en tu navegador web.
2. Selecciona tu cuenta educativa y autoriza los permisos de acceso para la CLI.
3. La terminal confirmará la sesión activa y guardará de forma cifrada el token en `~/.gemini/antigravity-cli/`.

Puedes consultar el estado de tu cuenta y los créditos disponibles con:

```bash
agy auth status
```

---

## 4. Filosofía Operativa de Antigravity CLI: Poda AST y Hardware Local ($0 Tokens)

Uno de los aspectos técnicos más fascinantes de Antigravity CLI es cómo utiliza los recursos de tu propia máquina (CPU Ryzen / Intel, memoria RAM y almacenamiento NVMe) para proteger tu cuota de tokens:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   ARQUITECTURA LOCAL DE ANTIGRAVITY CLI                │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Poda AST Determinística ──► Extrae firmas y contratos sin cuerpos  │
│ 2. Caché de Símbolos en RAM ─► Evita enviar archivos no relacionados  │
│ 3. Linters y Tests en CPU  ──► Ejecuta ruff y pytest localmente        │
│ 4. API de Frontera (Cloud)  ──► Recibe únicamente diffs quirúrgicos    │
└────────────────────────────────────────────────────────────────────────┘
```

El modelo remoto nunca lee archivos completos innecesarios; tu hardware local procesa el árbol de código y envía resúmenes ultra-compactos, garantizando que tu suscripción de 5 USD rinda al máximo.

---

## 5. Slash Commands y Atajos Esenciales en la Consola `agy`

Al iniciar una sesión con `agy`, ingresas al entorno interactivo de pair programming. Dispone de comandos especiales precedidos por barra (`/`):

| Comando | Función Principal |
| :--- | :--- |
| **`/help`** | Muestra el listado completo de atajos, variables y comandos disponibles. |
| **`/plan`** | Activa el modo de planificación estructurada paso a paso antes de editar código. |
| **`/browser`** | Inicia el motor de navegación web headless e interactivo (lo veremos en la Lección 3.5). |
| **`/clear`** | Limpia la pantalla y reinicia el contexto conversacional inmediato. |
| **`/stats`** | Muestra el consumo de tokens y llamadas de herramientas de la sesión actual. |
| **`/exit`** | Finaliza la sesión de Antigravity y retorna al prompt de Bash. |

---

## 6. Primer Ejercicio Guiado con `agy`

Ubicados en la carpeta de nuestro proyecto:

```bash
cd ~/proyectos_software/energy-ml
agy
```

Escribe la siguiente instrucción de prueba en el prompt interactivo:

> *"Inspecciona la estructura de `energy-ml` e indícame cuáles son los módulos principales en `src/` sin modificar ningún archivo."*

Observa cómo Antigravity CLI utiliza herramientas de introspección para listar la arquitectura del proyecto sin gastar tokens de escritura.

---

## 7. Conclusión

Con Antigravity CLI configurado bajo el plan estudiantil de 5 USD/mes, cuentas con una herramienta de potencia industrial adaptada a tu presupuesto académico.

En la siguiente lección, exploraremos el superpoder diferenciador de AGY: **el modo navegador (`/browser`)**, aprendiendo cómo los agentes pueden consultar documentación oficial en internet y validar datos en tiempo real mientras programamos en `energy-ml`.
