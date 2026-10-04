# 2.2 Requisitos No-Funcionales (NFR): performance, seguridad, escalabilidad

## Objetivo

Especificar **CÓMO** debe comportarse el sistema: velocidad, confiabilidad, seguridad. Ref: **spec**

## Contenidos

### 1. Tipos de NFR

```yaml
Performance:
  - Latencia de API < 200ms (p95)
  - Dashboard carga en < 3s
  - BD soporta 1000 req/seg

Escalabilidad:
  - Soportar 1000 usuarios concurrentes
  - BD crecimiento hasta 10GB sin degradación

Seguridad:
  - Autenticación: JWT tokens
  - Autorización: roles (admin, user, guest)
  - Encriptación: TLS en transporte, bcrypt en contraseñas

Disponibilidad:
  - Uptime >= 99.5%
  - RTO < 1 hora
  - RPO < 15 minutos

Mantenibilidad:
  - Código > 80% tipado (Pyright, spec)
  - Cobertura tests >= 85%
  - Documentación en README

Usabilidad:
  - UI responsiva (mobile-first)
  - Accesibilidad WCAG 2.1 AA
```

### 2. Ejemplo: Proyecto Energético

```
NFR-01: Performance de Dashboard
Descripción: Carga de última 24h en < 3s
Justificación: Usuarios revisan en la mañana, no toleran retrasos

NFR-02: Precisión de almacenamiento
Descripción: Pérdida de datos < 0.1%
Justificación: Datos críticos para facturación

NFR-03: Seguridad de acceso
Descripción: Solo gerente ve costos, técnico ve cargas
Justificación: Información sensible
```

### 3. Ejemplo: Proyecto Institucional

```
NFR-04: Escalabilidad
Descripción: Soportar 500 alumnos activos simultáneamente
Justificación: Picos en inscripción (enero-febrero)

NFR-05: Disponibilidad
Descripción: Uptime >= 99% (max 7.2h downtime/mes)
Justificación: Servicio crítico educativo
```

## Actividad Práctica

Escribir 3-5 NFR de tu proyecto. Incluir justificación.

## Palabras clave

NFR, performance, seguridad, escalabilidad, confiabilidad, mantenibilidad

## Referencias

- spec § Especificación de Requisitos (NFR section)
- https://en.wikipedia.org/wiki/Non-functional_requirement

