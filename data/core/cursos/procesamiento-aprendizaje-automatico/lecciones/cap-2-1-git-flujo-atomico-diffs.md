# Guía de Laboratorio: Capítulo 2 — Git como Fundamento del Trabajo con Agentes

**Curso:** Nivel 0 — Procesamiento y Aprendizaje Automático Inicial  
**Slug:** `procesamiento-aprendizaje-automatico-inicial`  
**Carga Horaria:** 2.5 - 3 Horas de Práctica Guiada  
**Requisitos Previos:** Manejo básico de terminal Bash (Capítulo 1), Python 3 y Git instalado.

---

## 🎯 Objetivos de Aprendizaje

Al finalizar este laboratorio, el estudiante estará capacitado para:
1. Comprender por qué **Git es la red de seguridad indispensable** cuando se trabaja con agentes de código (Aider, OpenCode, AGY CLI).
2. Analizar e interpretar cambios de código línea por línea mediante `git diff` antes de staging o commit.
3. Dominar el staging interactivo por fragmentos (`git add -p`) para seleccionar únicamente los cambios correctos e ignorar o descartar refactors innecesarios.
4. Aplicar un **Protocolo de Auditoría Anti-Aceptación Ciega** para evaluar sugerencias de IA sin comprometer la calidad ni la seguridad de la aplicación.
5. Mantener un historial de commits limpio, atómico y legible mediante `git log --oneline`.

---

## 📑 Marco Teórico Corto

### ¿Por qué Git es el escudo fundamental al programar con Agentes?
Los agentes de inteligencia artificial pueden escribir cientos de líneas de código en segundos. Sin embargo, también pueden:
- **Sobreescribir lógica existente** por malentender el contexto.
- **Introducir bugs sutiles** o cambiar convenciones de estilo del proyecto.
- **Inyectar credenciales o valores *hardcodeados*** en lugar de usar variables de entorno.

**Git** actúa como una cámara de congelamiento y auditoría. Cada commit representa un punto de restauración seguro. Si un agente genera un cambio defectuoso, Git permite aislar la falla, descartar los fragmentos problemáticos o revertir el estado del proyecto sin perder el trabajo previo.

---

## 🛠️ Parte 1: Configuración e Inicialización del Repositorio

### Paso 1.1: Configurar Identidad en Git (si no se realizó previamente)
Abre la terminal y verifica o define tu nombre y correo:

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@ejemplo.com"
```

### Paso 1.2: Inicializar el Proyecto de Práctica
Crea un directorio limpio para el laboratorio de Git y navega hacia él:

```bash
mkdir ~/lab_git_agentes
cd ~/lab_git_agentes
git init
```

### Paso 1.3: Crear la Estructura Base y Archivos Iniciales
Crea un script utilitario en Python `calculadora_datos.py` y un archivo `.gitignore`:

```bash
cat << 'EOF' > calculadora_datos.py
import math

def calcular_promedio(numeros):
    if not numeros:
        return 0.0
    return sum(numeros) / len(numeros)

if __name__ == "__main__":
    datos = [10.5, 20.0, 30.2, 40.8]
    print(f"Datos: {datos}")
    print(f"Promedio: {calcular_promedio(datos):.2f}")
EOF
```

Crea el archivo `.gitignore` para evitar rastrear archivos temporales o entornos virtuales:

```bash
cat << 'EOF' > .gitignore
.env
venv/
__pycache__/
*.pyc
EOF
```

### Paso 1.4: Primer Commit Base
Revisa el estado, añade los archivos e inicializa el historial:

```bash
git status
git add .
git commit -m "feat: inicializar script calculadora_datos y gitignore"
git log --oneline
```
