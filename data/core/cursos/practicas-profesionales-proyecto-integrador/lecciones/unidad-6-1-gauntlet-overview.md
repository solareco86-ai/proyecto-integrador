# 6.1 Constraint Gauntlet: 11 Validaciones según spec

## Objetivo

Entender el framework de verificación **Constraint Gauntlet**: 11 validaciones arquitectónicas y de seguridad que rodean el código con restricciones extremas. NO es "ser perfeccionista"; es **eliminar clases enteras de bugs antes de que ocurran**.

## Referencia

**spec § 5.2:** "Las 11 Baterías del Guantelete" (`tests/test_architecture.py`)

**spec § 5.5:** Matriz de Verificación Automatizada Previa a Despliegues

**Filosofía:** Robert C. Martin - "Mi estrategia es no leer el código generado. Lo que hago es rodearlo de restricciones extremas."

## Contenidos

### 1. ¿Qué es Constraint Gauntlet?

No es un test más. Es un **marco defensivo automático** que ejecuta antes de que código toque `main` (rama principal).

**Analogía:** Un corredor que cruza un "gauntlet" (línea de desafíos). Si falla UNO, no cruza. Si cruza todos, código es seguro.

**Beneficio:** Elimina clases **enteras** de bugs:
- SQL injection (validación #2)
- Hardcoded secrets (validación #1)
- Arquitectura quebrada (validación #4, #5)
- Dead code (complementario: test_clean_design.py)

### 2. Las 11 Validaciones (spec § 5.2)

Todas en `tests/test_architecture.py`. Se ejecutan: `python3 tests/test_architecture.py`

#### **#1: test_no_hardcoded_secrets**
```
Objetivo: Bloquea passwords, tokens JWT, API keys, connection strings quemadas en código.

Ejemplos MALO (detecta):
  - password = "admin123" (en variable)
  - db_url = "postgresql://user:pass@host" (literal)
  - api_key = "sk-abc123def456" (hardcodeado)

Ejemplos BUENO:
  - password = os.environ.get("DB_PASSWORD")  # lee de env
  - db_url = settings.DATABASE_URL  # lee de config.py

Por qué: Si código con secret entra a GitHub, secret está comprometido (incluso si después lo borrás).

Falla cuando: Encuentra strings sospechosos (30+ caracteres, patrón de token, etc.)
```

#### **#2: test_no_raw_sql_formatting**
```
Objetivo: Prohíbe f-strings o concatenación en SQL (SQL Injection OWASP).

Ejemplos MALO (detecta):
  query = text(f"SELECT * FROM users WHERE id = {user_id}")
  query = text("SELECT * FROM users WHERE id = " + str(user_id))

Ejemplos BUENO:
  query = text("SELECT * FROM users WHERE id = :id").bindparams(id=user_id)
  # SQLAlchemy parametriza automáticamente

Por qué: Si user_id viene de usuario malicioso:
  user_id = "1 OR 1=1"  # SQL injection
  Query se convierte en: "SELECT * FROM users WHERE id = 1 OR 1=1"  (devuelve todo)

Falla cuando: Detecta f-strings o + en text(...)
```

#### **#3: test_no_os_environ_direct_access**
```
Objetivo: Centraliza acceso a variables de entorno. Solo en src/infrastructure/settings/config.py

Ejemplos MALO (detecta):
  # En application/services/user_service.py
  db_host = os.environ.get("DB_HOST")  # ❌ Acceso directo

Ejemplos BUENO:
  # En infrastructure/settings/config.py
  class Settings:
      db_host: str = os.environ.get("DB_HOST")
  
  # En application/services/user_service.py
  from src.infrastructure.settings import settings
  db_host = settings.db_host  # ✅ Indirecto

Por qué: Centralizar permite:
  - Un lugar para validar (¿env var existe?, ¿formato correcto?)
  - Cambiar source (env → archivo .env → Vault) sin tocar código

Falla cuando: Encuentra import de os y llamadas a os.environ/os.getenv fuera de config.py
```

#### **#4: test_domain_isolation**
```
Objetivo: Domain (src/domain) es 100% puro. CERO dependencias externas.

Ejemplos MALO (detecta):
  # En src/domain/entities/user.py
  from pydantic import BaseModel  # ❌ Pydantic es externa
  from sqlalchemy import Column  # ❌ ORM es externa
  import requests  # ❌ HTTP es externa

Ejemplos BUENO:
  # En src/domain/entities/user.py
  from dataclasses import dataclass
  from datetime import datetime
  
  @dataclass
  class User:
      id: int
      email: str
      created_at: datetime
  
  # Solo stdlib + tipos puro

Por qué: Domain debe ser "portable". Si cambias framework (FastAPI → Django), Domain NO cambia.

Falla cuando: Encuentra imports de cualquier librería externa (no stdlib) en src/domain/
```

#### **#5: test_application_and_adapters_layers**
```
Objetivo: Valida 4 capas y regla de dependencia (no "upward").

Regla: Domain ← Application ← Adapters,Infrastructure
       (sin reversa)

Ejemplos MALO (detecta):
  # En src/domain/user.py
  from src.application.services import UserService  # ❌ Domain depende de Application (upward)

Ejemplos BUENO:
  # Domain: solo lógica pura
  # Application: llama a Domain
  # Adapters: presenters, repositorio abstracto
  # Infrastructure: implementación concreta (FastAPI, DB)

Por qué: Arquitectura limpia = dependencias hacia adentro (hacia Domain). Nunca hacia afuera.

Falla cuando: Detecta imports que violan regla de dependencia
```

#### **#6: test_function_return_types**
```
Objetivo: 100% de funciones en Domain y Application DEBEN tener -> Type

Ejemplos MALO (detecta):
  # En src/domain/services/calculation.py
  def calculate_fee(amount):  # ❌ Sin tipo retorno
      return amount * 0.1

Ejemplos BUENO:
  def calculate_fee(amount: float) -> float:
      return amount * 0.1

Por qué: Sin tipo retorno, Pyright no puede verificar usos posteriores. Bugs silenciosos.

Falla cuando: Encuentra funciones sin -> Type en src/domain/ y src/application/
```

#### **#7: test_function_arg_types**
```
Objetivo: 100% de parámetros en Domain y Application DEBEN tener tipos.

Ejemplos MALO (detecta):
  def validate_email(email):  # ❌ Sin tipo
      return "@" in email

Ejemplos BUENO:
  def validate_email(email: str) -> bool:
      return "@" in email

Por qué: Mismo que #6. Type safety.

Falla cuando: Encuentra parámetros sin type hint
```

#### **#8: test_init_files_must_be_empty**
```
Objetivo: Todos los __init__.py en src/ y tests/ DEBEN estar vacíos (0 bytes).

Ejemplos MALO (detecta):
  # src/domain/__init__.py
  from .entities import User  # ❌ Tiene código
  from .value_objects import Email

Ejemplos BUENO:
  # src/domain/__init__.py
  # (archivo completamente vacío, 0 bytes)

Por qué: imports en __init__ crean ciclos circulares, hacen imports implícitos. Mejor explícitos.

Falla cuando: __init__.py no está vacío
```

#### **#9: test_no_relative_imports**
```
Objetivo: Solo imports absolutos. Prohibe relative imports (from . import X)

Ejemplos MALO (detecta):
  # En src/application/services/user_service.py
  from . import entities  # ❌ Relative
  from ..domain import User  # ❌ Relative

Ejemplos BUENO:
  from src.application import entities
  from src.domain import User

Por qué: Relative imports rompen con refactors. Absolutos son explícitos y seguros.

Falla cuando: Detecta from . o from .. en src/
```

#### **#10: test_no_unstructured_prints**
```
Objetivo: Bloquea print() en código de producción. Solo logging.

Ejemplos MALO (detecta):
  # En src/application/services/user_service.py
  print(f"User created: {user.id}")  # ❌ print en prod

Ejemplos BUENO:
  import logging
  logger = logging.getLogger(__name__)
  logger.info(f"User created: {user.id}", extra={"user_id": user.id})

Por qué: print() no es configurable. Logging sí: nivel, formato, destino, contexto.

Falla cuando: Detecta print( en src/ (excepto scripts de test)
```

#### **#11: test_relative_path_headers**
```
Objetivo: Cada archivo .py en src/ y tests/ DEBE comenzar con docstring/comentario con su ruta relativa.

Ejemplos MALO (detecta):
  # src/domain/entities/user.py
  from dataclasses import dataclass
  ...

Ejemplos BUENO:
  """
  src/domain/entities/user.py
  
  Entidad User del dominio.
  """
  from dataclasses import dataclass
  ...

Por qué: Cuando error en test output, ves la ruta exacta sin ambigüedades.

Falla cuando: Archivo no empieza con docstring que contiene su ruta
```

### 3. Complementarios: Dead Code & Componentes Dios

**test_clean_design.py** detecta:
- UNREACHABLE_FILE: archivos .py huérfanos
- GHOST_INTERFACE: Protocol/ABC con 1 sola implementación (YAGNI)
- MIDDLE_MAN_METHOD: métodos que solo delegan sin valor
- DEEP_INHERITANCE: herencia > 2 niveles
- ORPHAN_PRIVATE_SYMBOL: funciones/métodos privados nunca usados
- SPECULATIVE_MICRO_FILE: archivos < 10 LOC dispersados

**test_god_components.py --strict** detecta:
- Clases demasiado grandes (monolitos)
- Baja cohesión (responsabilidades variadas)
- Bajo acoplamiento (demasiadas dependencias)

### 4. Matriz de Verificación Completa (spec § 5.5)

Se ejecutan todos ANTES de que código entre a main:

```bash
# 1. Linter y Formato
ruff check .
ruff format --check .

# 2. Tipado Estricto
pyright src/

# 3. Constraint Gauntlet (11 validaciones)
python3 tests/test_architecture.py

# 4. Componentes Dios
python3 tests/test_god_components.py --strict

# 5. Código Muerto & Sobreingeniería
python3 tests/test_clean_design.py --strict

# 6. Tests (unit, integration, E2E)
pytest --maxfail=1 --disable-warnings -v
```

**Si UNO falla:** Código NO entra a main. Developer arregla y reintenta.

### 5. Ejemplo: Energy-ML

**¿Qué valida el Gauntlet?**

```python
# ❌ Validación #1 falla:
db_url = "postgresql://user:password123@localhost"  # Secret hardcodeado

# ❌ Validación #2 falla:
query = text(f"SELECT * FROM readings WHERE user_id = {user_id}")  # SQL Injection

# ❌ Validación #3 falla:
# En src/application/services/reading_service.py
api_key = os.environ.get("API_KEY")  # Debe estar en config.py

# ❌ Validación #4 falla:
# En src/domain/entities/reading.py
from pydantic import BaseModel  # Domain no puede tener dependencias

# ✅ Paso:
# src/domain/entities/reading.py (puro, sin dependencias)
@dataclass
class Reading:
    timestamp: datetime
    power_kw: float
    
    def is_anomaly(self, avg_kw: float) -> bool:
        return self.power_kw > avg_kw * 1.2
```

## Actividad Práctica

1. **Corre el Gauntlet en tu proyecto (Semana 14-15):**
   ```bash
   # 1. Verifica cada validación
   python3 tests/test_architecture.py
   python3 tests/test_god_components.py --strict
   python3 tests/test_clean_design.py --strict
   
   # 2. Si falla, lee el error
   # 3. Arregla (los detalles vienen en mensajes)
   # 4. Reintenta
   ```

2. **Documenta en `GAUNTLET_REPORT.md`:**
   ```markdown
   # Constraint Gauntlet - Sprint 2
   
   ## Validación 1: No Hardcoded Secrets
   - Status: ✅ PASS
   - Issues found: 0
   - Details: Zero secrets detected
   
   ## Validación 2: No Raw SQL
   - Status: ✅ PASS
   - Issues found: 0
   
   ... (repite para cada una)
   
   ## Resumen
   - Total validaciones: 11
   - Pasadas: 11 ✅
   - Fallidas: 0
   - Score: 100%
   ```

3. **Integra en pre-push:**
   ```bash
   # .git/hooks/pre-push incluye:
   echo "Running Constraint Gauntlet..."
   python3 tests/test_architecture.py || exit 1
   python3 tests/test_god_components.py --strict || exit 1
   python3 tests/test_clean_design.py --strict || exit 1
   ```

## Palabras clave

Constraint Gauntlet, Validación de Arquitectura, Security, Type Safety, Domain Isolation, Code Quality, AST Analysis, Deterministic Verification

## Referencias

- spec § 5.2 (Las 11 Baterías)
- spec § 5.5 (Matriz de Verificación)
- https://github.com/datamaq-automation/spec/tree/main/backend/template/tests
- Robert C. Martin, "Clean Architecture"
