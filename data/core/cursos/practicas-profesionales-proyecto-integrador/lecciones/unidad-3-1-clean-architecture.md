# 3.1 Clean Architecture: 4 capas, 7 reglas innegociables (spec)

## Objetivo

Diseñar arquitectura del proyecto siguiendo Clean Architecture y spec.

## Referencia

**spec/backend/srs-spec-backend-fastapi.md § Stack Tecnológico y Arquitectura**

https://github.com/datamaq-automation/spec/blob/main/backend/srs-spec-backend-fastapi.md

## Contenidos

### 1. Las 4 Capas (Uncle Bob)

```
┌─────────────────────────────────────┐
│  UI / Controllers / REST API        │  (Infrastructure)
├─────────────────────────────────────┤
│  Application Services / Use Cases   │  (Application)
├─────────────────────────────────────┤
│  Domain / Entities / Business Rules │  (Domain)
├─────────────────────────────────────┤
│  Frameworks / DB / External APIs    │  (Infrastructure)
└─────────────────────────────────────┘
```

### 2. Las 7 Reglas Innegociables (spec)

1. **Aislamiento de capas:** Domain sin dependencias externas
2. **Inyección de dependencias:** No hardcodeo de conexiones
3. **Tipado exhaustivo:** Pyright sin errores (spec)
4. **Tests:** >= 85% cobertura (pytest)
5. **Commits atómicos:** Cada cambio es reversible
6. **Logging estructurado:** No print(), usar logger
7. **Validación en bordes:** DTOs en adapters, not en domain

### 3. Estructura de directorios (spec)

```
src/
├── domain/              (Entidades, value objects, sin dependencias)
│   ├── energetica/
│   │   ├── entities.py
│   │   └── value_objects.py
│   └── academica/
│       ├── entities.py
│       └── value_objects.py
├── application/         (Servicios, DTOs, use cases)
│   ├── services/
│   ├── dtos/
│   └── mappers/
├── adapters/            (Presenters, repositorio abstracto)
│   └── presenters/
└── infrastructure/      (FastAPI, DB, configs)
    ├── fastapi/
    ├── db/
    └── config.py
```

## Actividad Práctica

Diseñar estructura de directorios para tu proyecto. Dibujar diagrama de capas y dependencias.

## Palabras clave

Clean Architecture, capas, aislamiento, inyección de dependencias

## Referencias

- spec § Stack Tecnológico y Arquitectura
- https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html

