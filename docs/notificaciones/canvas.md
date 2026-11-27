# Canvas — Sistema de notificaciones del campus

**Autor:** Lautaro Amengual · **Proyecto:** ISFT N.º 199 · **Fecha:** 17/11/2026  
**Estado:** Reconstrucción de la propuesta previa; módulo discontinuado junto con el campus.

## Problema

La propuesta partía de la necesidad de comunicar publicaciones de noticias, eventos y comunicados, y eventos de preinscripción, a los destinatarios pertinentes. Según las issues #44–#49, existían alertas operativas de contactos a destinatarios fijos, pero no una bandeja personal, suscripciones ni historial de entregas por persona. Esto limitaba la posibilidad de consultar avisos propios y controlar qué comunicaciones recibir. La magnitud del problema no había sido medida con usuarios.

## Destinatarios y propuesta de valor

Los beneficiarios previstos eran usuarios del campus y, según la definición funcional pendiente, aspirantes/preinscriptos y personal institucional autorizado. La propuesta era reunir avisos personales en un lugar consultable, respetar preferencias por canal y permitir revisar fallas de entrega. Los destinatarios concretos de cada evento requerían aprobación institucional en #44.

## Solución propuesta

| Componente | Función prevista |
|---|---|
| Bandeja en el campus | Consultar avisos propios y distinguir leídos de no leídos. |
| Suscripciones | Gestionar preferencias y bajas según las reglas aprobadas. |
| Email y Telegram | Complementar la bandeja mediante los canales habilitados. |
| Historial | Registrar resultados por canal; panel administrativo sujeto a aprobación. |
| Disparadores | Generar avisos en la primera publicación y ante una preinscripción válida. |

El enfoque técnico contemplaba reutilizar transportes existentes, agregar persistencia compatible con SQLite/MySQL y mantener la arquitectura limpia. No incluía push móvil, SMS, WhatsApp ni un servicio de colas nuevo.

## Métricas de éxito propuestas

Estas metas se proponen en esta reconstrucción para hacer evaluable la idea; no eran resultados obtenidos ni compromisos aprobados en las issues.

| Indicador | Meta propuesta | Medición prevista |
|---|---|---|
| Avisos duplicados | 0 duplicados por origen, destinatario y canal en los casos de prueba | Antes del piloto, reprocesando eventos. |
| Respeto de bajas opcionales | 100 % de los casos sin nuevos envíos tras la baja | Antes del piloto y revisión semanal durante cuatro semanas. |
| Aislamiento entre usuarios | 0 accesos indebidos en los casos de autorización | Antes del piloto y ante cambios de permisos. |
| Trazabilidad de entregas | 100 % de los intentos del piloto con canal y resultado registrados | Revisión semanal durante cuatro semanas. |
| Uso de la bandeja | Al menos 80 % de participantes completa consultar y marcar un aviso sin ayuda | Una sesión de prueba al finalizar el primer mes de piloto; registrar tamaño de muestra. |

## Recursos, sostenimiento y validación pendiente

Se necesitaban desarrollo, revisión institucional, pruebas con usuarios, alojamiento y operación de los canales. No se habían estimado costos ni aprobado financiación. La propuesta no contemplaba cobros a estudiantes. Antes del piloto debían resolverse identidad, permisos, destinatarios, consentimiento, conservación de datos y vinculación segura de Telegram.

## Decisión final

Se discontinuó el campus, donde iba a vivir el módulo. En consecuencia, las issues #44–#49 se cerraron como **no planificadas** el 17/11/2026. El piloto y las mediciones aquí propuestos no se realizaron como parte de este módulo.

**Fuentes:** [Épica #45 y tareas vinculadas](https://github.com/solareco86-ai/proyecto-integrador/issues/45) · [Definiciones pendientes #44](https://github.com/solareco86-ai/proyecto-integrador/issues/44) · [Guía de Canvas de la materia: problema, solución y métricas](https://github.com/solareco86-ai/proyecto-integrador/blob/main/data/core/cursos/practicas-profesionales-proyecto-integrador/lecciones/unidad-1-1-canvas-problema-solucion.md).
