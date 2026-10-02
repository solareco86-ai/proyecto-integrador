# Guía de Laboratorio — Capítulo 3: La Tríada de Asistentes (Aider, OpenCode y AGY CLI)

**Asignatura:** Nivel 0 — Procesamiento y Aprendizaje Automático Inicial  
**Slug:** `procesamiento-aprendizaje-automatico-inicial`  
**Carga horaria estimada:** 2.5 horas  
**Prerrequisitos:** Haber completado las Guías de Laboratorio 1 (Terminal y Entornos Virtuales) y 2 (Git y Auditoría de Código).

---

## 1. Objetivos de Aprendizaje

Al finalizar este laboratorio, el estudiante será capaz de:
1. Instalar y configurar asistentes de código basados en consola (**Aider**, **OpenCode** y **AGY CLI**).
2. Comprender la **anatomía de una instrucción técnica (prompt)** para guiar de forma precisa a un agente de código.
3. Acotar el contexto suministrado al agente para prevenir alucinaciones y consumo innecesario de tokens.
4. Construir un script utilitario en Python guiado paso a paso por **Aider**, realizando peticiones de generación, refactorización y explicación.
5. Aplicar un flujo continuo de auditoría previa mediante Git antes de consolidar los cambios sugeridos por la IA.

---

## 2. Marco Teórico: La Tríada de Asistentes CLI

A diferencia de los chats web convencionales, los asistentes de línea de comandos interactúan directamente con el sistema de archivos y el árbol de trabajo de Git:
* **Aider:** Asistente especializado en edición directa de archivos en repositorios Git. Realiza commits automáticos o semi-automáticos con mensajes descriptivos.
* **OpenCode:** Herramienta enfocada en la generación modular y refactorización rápida de scripts.
* **AGY CLI:** Herramienta de asistencia en consola con capacidades avanzadas de inspección y contexto acotado.

---

## 3. Desarrollo Práctico: Preparación y Repositorio

### Paso 1: Preparación del Entorno e Instalación

1. Abre tu terminal Bash y navega a la carpeta de trabajo:
   ```bash
   cd ~/curso-ia/nivel-0
   source venv/bin/activate
   ```

2. Verifica las variables de entorno para asegurar que las API Keys necesarias estén cargadas:
   ```bash
   python -c "import os, dotenv; dotenv.load_dotenv(); print('API Key configurada:', bool(os.getenv('OPENAI_API_KEY') or os.getenv('ANTHROPIC_API_KEY')))"
   ```

3. Instala los asistentes requeridos en tu entorno virtual:
   ```bash
   pip install aider-chat
   ```

### Paso 2: Creación del Repositorio de Trabajo

1. Crea un directorio limpio para el laboratorio e inicializa Git:
   ```bash
   mkdir lab3_asistentes
   cd lab3_asistentes
   git init
   ```

2. Crea un archivo de logs sintético para las pruebas (`app.log`):
   ```bash
   cat << 'EOF' > app.log
   2026-09-18 08:00:12 [INFO] Servidor iniciado correctamente en puerto 8000.
   2026-09-18 08:01:45 [WARNING] Uso de memoria elevado: 82%.
   2026-09-18 08:02:10 [ERROR] Conexión rechazada por la base de datos PostgreSQL.
   2026-09-18 08:03:00 [INFO] Solicitud GET /healthcheck respondida 200 OK.
   2026-09-18 08:05:22 [CRITICAL] Fallo de memoria no gestionado en proceso 4102.
   2026-09-18 08:06:11 [ERROR] Timeout al consultar la API externa de pagos.
   EOF
   ```

3. Guarda el estado inicial en Git:
   ```bash
   git add app.log
   git commit -m "docs: agregar archivo de logs de prueba"
   ```
