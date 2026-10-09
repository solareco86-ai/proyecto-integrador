# 5B.2 Desarrollo Limpio según Spec: Commits Atómicos, PRs, Code Review

## Objetivo

Escribir código que respete Clean Architecture. Commits deben ser atómicos (reversibles, claros). Pull Requests (PRs) deben tener descripción y pasar code review. Esto NO es "ser perfeccionista"; es respetar a quien va a mantener tu código.

## Referencia

**Unidad 3.1:** Clean Architecture (4 capas, 7 reglas)

**spec:** § Stack Tecnológico (Clean Architecture, commits, PRs)

## Contenidos

### 1. Clean Code: Las 7 Reglas de spec

Recordatorio (Unidad 3.1):

1. **Aislamiento de capas:** Domain sin dependencias externas ✅ (sin Pydantic, FastAPI)
2. **Inyección de dependencias:** No hardcodeamos conexiones
3. **Tipado exhaustivo:** Pyright sin errores (Python)
4. **Tests:** >= 85% cobertura (pytest)
5. **Commits atómicos:** Cada cambio reversible
6. **Logging estructurado:** No `print()`, usar `logger`
7. **Validación en bordes:** DTOs en adapters, NO en domain

**Verificación:**
```bash
npm run typecheck:js      # TypeScript LSP: 0 errores
pyright                   # Python: 0 errores
pytest --cov=src --cov-fail-under=85
python3 scripts/verify_architecture.py
```

### 2. Commits Atómicos: El Arte de la Reversibilidad

**¿Qué es atómico?**

Cada commit es **una idea completa**. Si revertimos ese commit con `git revert`, el código sigue siendo válido (no quebrado).

**MALO (commit "comilón"):**
```
commit abc1234
  fix: Mil cosas

  - Agregué validación de email
  - Refactoricé post-procesamiento
  - Agregué tests
  - Cambié requirements.txt
  - Arreglé bug en OCR

Problema: Si otros cambios rompieron algo, ¿cual de estos fue?
No puedes revertir solo "validación email" sin revertir todo.
```

**BUENO (commits pequeños, enfocados):**
```
commit feat1: feat(domain): agregar validación de email
  Cambio pequeño: solo la lógica de validación en domain/

commit feat2: refactor(application): reorganizar post-procesamiento
  Cambio: solo refactor, comportamiento idéntico

commit feat3: test(application): tests para post-procesamiento
  Cambio: solo tests

commit feat4: chore: actualizar requirements.txt con librería X
  Cambio: solo actualizó versiones

Si en feat2 se introdujo bug, revertimos solo feat2. Resto se mantiene.
```

### 3. Anatomía de un Buen Commit

**Mensaje (Conventional Commits):**
```
type(scope): descripción breve (< 50 caracteres)

Descripción detallada (si es necesario).
Explica QUÉ y POR QUÉ, no CÓMO.

Refs: #issue-123
Co-Authored-By: ...
```

**Tipos:**
- `feat:` nueva funcionalidad
- `fix:` bug fix
- `refactor:` código cambió, comportamiento igual
- `test:` agregó tests
- `chore:` tareas administrativas (dependencias, config)
- `docs:` documentación

**Scope:**
- `domain:` cambios en entidades, lógica pura
- `application:` servicios, DTOs, mappers
- `adapters:` presenters, adaptadores de interfaz
- `infrastructure:` FastAPI, DB, config

**Ejemplos:**
```
feat(domain): agregar DDD entity Usuario con validaciones

fix(application): NLP no procesa strings vacíos

refactor(infrastructure): mover config de BD a variable de entorno

test(adapters): tests de presenter JSON

docs: actualizar README con instrucciones de setup
```

### 4. Pull Request (PR) Workflow

**Paso 1: Crear rama**
```bash
git checkout -b feat/ocr-integration
```

**Paso 2: Código limpio (durante el sprint)**
- Commits atómicos
- Typecheck: `pyright` sin errores
- Tests: `pytest` >= 85% cobertura
- Linters: `ruff check`, `black` (reformatean código)

**Paso 3: Pre-push validation (hook automático)**
```bash
# .git/hooks/pre-push ejecuta:
npm run typecheck:js
pyright
pytest --cov=src --cov-fail-under=85
python3 scripts/verify_architecture.py

# Si algo falla, no pushea. Arreglas localmente, reintentas.
```

**Paso 4: Crear PR en GitHub**
```bash
git push -u origin feat/ocr-integration

# En GitHub UI:
  Title: "feat(application): integrar OCR con pipeline"
  Description:
    ## Summary
    - OCR ahora se llama desde pipeline de datos
    - DTOs entre componentes definidas
    - Tests de integración para OCR→NLP
    
    ## Test Plan
    - [ ] OCR procesa imagen de ejemplo correctamente
    - [ ] DTO se pasa correctamente a NLP
    - [ ] Error handling si OCR falla
    
    Fixes #123
```

**Paso 5: Code Review**
- Mínimo 1 persona revisa
- Comenta líneas específicas
- Autor responde (sin defensividad)
- Se itera hasta OK

**Ejemplo de Code Review (Bueno):**
```
Reviewer (Dev2): "Lindo, pero ¿por qué no separamos esta función en 2?
Sería más fácil de testear."

Autor (Dev1): "Buena idea. Separo en ocr_read() + ocr_validate()."

[Dev1 hace commit `refactor: separar OCR en read/validate`]

Reviewer: "Perfecto. ✅ Aprobado"
```

**Ejemplo de Code Review (Malo):**
```
Reviewer: "Este código es un desastre."

Autor: "¿QUÉ? Yo lo hice bien!"

[Conflicto. Nadie aprende.]
```

**Paso 6: Merge**
```bash
# En GitHub: Click "Merge pull request"
# Estrategia: "Squash and merge" (1 commit limpio) O "Rebase and merge"
# NO "Create a merge commit" (historial sucio)
```

### 5. Code Review: Critique sin Culpa

La clave es **separar código de persona**.

**MALO:**
```
"Esto está mal."     ← Juzga código + persona
```

**BUENO:**
```
"¿Consideraste hacer X en lugar de Y? Así sería más..."  ← Pregunta, sugerencia
```

**En Code Review, observar:**
1. **Clean Architecture:** ¿Las 4 capas se respetan?
2. **Tipado:** ¿Pyright 0 errores?
3. **Testing:** ¿Tests? ¿Cubren el caso?
4. **Nombrado:** ¿Variables comunican intención?
5. **Logging:** ¿Usa logger, no print()?

**Preguntas útiles:**
- "¿Por qué elegiste estructura X en lugar de Y?"
- "¿Este DTO es consistente con los otros?"
- "¿Qué pasa si input es vacío/None?"
- "¿Hay test para this edge case?"

### 6. Commits Frecuentes: No Esperes a "Terminar"

**MALO (commits raros):**
```
Lunes: Start feature
Miércoles: Commit gigante con 500 líneas
Viernes: Otro commit gigante
```

Problema: Cambios no están backedup. Si pierde laptop, pierde trabajo.

**BUENO (commits diarios):**
```
Lunes 20:00: commit "feat: estructura base de OCRService"
Martes 20:00: commit "feat(ocr): integrarse con Tesseract"
Miércoles 20:00: commit "test(ocr): tests unitarios de OCR"
Jueves 20:00: commit "refactor(ocr): código más limpio"
Viernes 16:00: commit "fix(ocr): bug en manejo de PDFs"
```

Ventajas:
- Backup diario (en GitHub)
- Historia clara de cambios
- Si algo rompe, es último commit
- Team puede ver progreso

### 7. Herramientas de Ayuda

**Linters automáticos:**
```bash
# Python
ruff check src/                    # Detecta errors, style issues
black src/                         # Reformatea código

# JavaScript
npm run lint                       # ESLint + Prettier

# Ambos mejoran **consistencia**, no **lógica**
# Si 2 personas codean, código se ve igual.
```

**Pre-commit hooks (local):**
```bash
# .git/hooks/pre-commit ejecuta:
#  - formateo (black, prettier)
#  - linters (ruff, eslint)
# Si falla, no allows commit. Arreglas, reintentas.
```

**CI/CD (en GitHub):**
```yaml
# .github/workflows/test.yml ejecuta cuando pusheas PR:
#  - Typecheck (pyright, tsc)
#  - Linters (ruff, eslint)
#  - Tests (pytest, jest)
#  - Coverage (pytest --cov)
# Si falla, PR muestra rojo. Debes arreglarlo.
```

## Actividad Práctica

1. **Setup local (antes de Sprint 1):**
   ```bash
   # Instalar pre-push hook
   cp scripts/pre-push.sh .git/hooks/pre-push
   chmod +x .git/hooks/pre-push
   
   # Verificar linters
   pyright src/ scripts/ tests/
   ruff check src/
   ```

2. **Durante cada sprint, al menos 1x al día:**

```bash
# Escribo código...
git add src/
git commit -m "feat(domain): agregar validación de email"
git push    # Pre-push hook valida automáticamente
```

3. **Al terminar feature (crear PR):**
   ```bash
   # En GitHub: New Pull Request
   Title: feat(application): integración OCR
   Description: [Summary, test plan, references]
   
   # Esperar code review
   # Responder a comentarios
   # Merge cuando aprobado
   ```

4. **Documentar proceso en `DEVELOPMENT_GUIDELINES.md`:**
   ```markdown
   # Desarrollo Clean

   ## Commits
   - Atómicos: una idea por commit
   - Mensaje: type(scope): descripción
   - Frecuencia: mínimo 1 commit/día

   ## PRs
   - 2-5 commits típicamente
   - Descripción: qué, por qué, cómo testear
   - Code review: mínimo 1 aprobador

   ## Quality Gates
   - Pyright 0 errores
   - Tests >= 85% cobertura
   - Linters passing
   - 4 capas de Clean Architecture respetadas
   ```

## Palabras clave

Commits atómicos, PR, Code review, Clean Code, Conventional Commits, Linters, Pre-push hooks, CI/CD

## Referencias

- spec § Stack Tecnológico
- Conventional Commits: https://www.conventionalcommits.org/
- GitHub Flow: https://guides.github.com/introduction/flow/
- Robert C. Martin, "Clean Code"
