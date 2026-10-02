# Guía de Laboratorio: Capítulo 2 — Git como Fundamento del Trabajo con Agentes

**Curso:** Nivel 0 — Procesamiento y Aprendizaje Automático Inicial  
**Slug:** `procesamiento-aprendizaje-automatico-inicial`  
**Carga Horaria:** 2.5 - 3 Horas de Práctica Guiada  

---

## 🧹 Parte 4: Limpieza de Código Rechazado y Commit Auditado

### Paso 4.1: Descartar Modificaciones Inseguras del Working Tree
Descarta los cambios no agregados al staging para limpiar el archivo:

```bash
git checkout -p calculadora_datos.py
# O en versiones recientes de Git:
# git restore -p calculadora_datos.py
```
Selecciona `y` para revertir los fragmentos que contienen la API Key y el log inseguro.

### Paso 4.2: Confirmar Estado del Archivo
Verifica que el script funciona sin exponer credenciales:

```bash
python3 calculadora_datos.py
```

### Paso 4.3: Realizar el Commit Auditado
Escribe un mensaje claro que refleje el cambio verificado:

```bash
git commit -m "feat: agregar funcion calcular_desviacion_estandar validada"
```

### Paso 4.4: Revisión del Historial Ejecutivo
Comprueba el registro histórico limpio:

```bash
git log --oneline --graph
```

---

## 📋 Lista de Cotejo / Rúbrica de Evaluación

| Criterio de Evaluación | Requisito Esperado | Puntaje |
| :--- | :--- | :---: |
| **Inicialización y Gitignore** | Repositorio iniciado con `.gitignore` correcto para Python y `.env`. | 20% |
| **Diagnóstico de Cambios** | Uso fluido de `git status` y lectura analítica de `git diff`. | 20% |
| **Auditoría Interactiva (`git add -p`)** | Capacidad de aislar fragmentos válidos de propuestas inseguras o alucinadas por IA. | 30% |
| **Depuración y Restauración** | Eliminación efectiva de código inseguro/hardcodeado sin afectar funciones válidas. | 15% |
| **Historial y Commits** | Commits atómicos con mensajes claros según convenciones (`feat:`, `fix:`). | 15% |

---

## 💡 Próximo Paso
Con los fundamentos de Git y auditoría consolidada, estamos listos para conectar las herramientas CLI de agentes en el **Capítulo 3: La Tríada de Asistentes (Aider, OpenCode y AGY CLI)**.
