# 01 — Diagnóstico Operativo y Hallazgos Estratégicos

> **Fecha:** 14 de Agosto de 2026  
> **Área:** Dirección Estratégica / Grupo DataMaq  
> **Contexto:** Evaluación de inversión para escalamiento de servicios independientes en AMBA.

---

## 1. Situación de Partida

* **Estabilidad de Base:** Trabajo formal bajo relación de dependencia que cubre el costo de vida fijo y reduce el riesgo de insolvencia financiera.
* **Capacidad Operativa:** Disponibilidad para tomar contratos y trabajos independientes de alto margen en horarios complementarios y fines de semana.
* **Activos Clave Existentes:**
  * **Movilidad:** Moto propia para traslados ágiles en el corredor norte de AMBA (evitando congestiones y con bajo costo de combustible/mantenimiento).
  * **Herramental:** Instrumental de medición propio disponible (multímetros, pinzas, instrumental de verificación eléctrica).
  * **Expertise Técnico:** Capacidad probada en instalaciones eléctricas, submedición de energía, electrónica industrial y desarrollo de software.

---

## 2. Cuellos de Botella Críticos Identificados

### 🚨 Cuello de Botella 1: Falta de Identidad Presencial y Ropa Desgastada
* **Problema:** Asistir a plantas industriales, comercios o consorcios con indumentaria desgastada, genérica o con logos de antiguos empleadores genera una fricción severa de confianza.
* **Impacto Económico:** El cliente percibe al profesional como "mano de obra informal" o "técnico tercerizado de segunda línea" en lugar de un **proveedor de ingeniería / consultor especializado**. Esto deprime los honorarios hasta un **40-50%** y dificulta el cierre de contratos corporativos.
* **Solución Inmediata:** Unificar la indumentaria de trabajo bajo la marca **DataMaq** (chombas/camisas bordadas, pantalones técnicos reforzados, abrigo softshell con reflectivos y calzado dieléctrico certificado).

### 🚨 Cuello de Botella 2: Ausencia de Canal de Captación Digital Activo
* **Problema:** No existe pauta publicitaria ni presencia geolocalizada activa que canalice la demanda caliente que busca servicios en Google diariamente.
* **Impacto Económico:** Dependencia exclusiva del boca a boca o contactos esporádicos, dejando pasar la ola de demanda generada por el sinceramiento y aumento de tarifas eléctricas en el AMBA.
* **Solución Inmediata:** Activación de **Google Ads (Búsqueda)** con términos de alta intención de compra y optimización de **Google Business Profile (Google Maps)** en Zona Norte.

---

## 3. Servicios Punta de Lanza y Oportunidades de Mercado

### A. Instalación de Medidores de Energía y Submedición (Punta de Lanza 🔥)
* **Contexto de Mercado:** Con el aumento de tarifas eléctricas y segmentación en AMBA, las industrias, parques industriales, galerías comerciales y consorcios necesitan urgentemente:
  1. Identificar consumos ocultos y picos de potencia.
  2. Sub-medir consumos individuales por inquilino o sector productivo para prorratear costos de forma justa.
  3. Corregir factor de potencia (coseno de phi) para evitar penalizaciones en factura.
* **Modelo de Negocio:** Cobro por relevamiento + instalación/conexionado de medidores + configuración de telemetría + reporte técnico mensual recurrente.

### B. Consultoría Energética y Mantenimiento Electrónico
* Diagnóstico de tableros eléctricos, mantenimiento de variadores de frecuencia (VFD), servomotores y placas de control.
* Mantenimiento preventivo programado a pymes que no tienen departamento de electromecánica propio.

### C. Desarrollo de Software a Medida & Telemetría IoT
* Dashboards web para visualización de energía en tiempo real (integrables a `datamaq.com.ar`).
* Sistemas SCADA livianos y automatizaciones de procesos mediante microcontroladores/PLCs y APIs.

---

## 4. Evaluación Técnica y Financiera de la GPU para Inteligencia Artificial

El usuario planteó adquirir una placa GPU para reducir costos en uso de IA (pre y post procesamiento de tokens hacia la API de DeepSeek mediante OpenCode).

```
┌────────────────────────────────────────────────────────────────────────┐
│                   ANÁLISIS DE INVERSIÓN EN GPU LOCAL                   │
├──────────────────────────────┬─────────────────────────────────────────┤
│ Por Ahorro de Tokens API     │ ❌ NO se amortiza en el corto plazo     │
│ (DeepSeek V3/R1 es ultra-barato: ~$0.14-$0.28 por 1M tokens)          │
├──────────────────────────────┼─────────────────────────────────────────┤
│ Por Productividad & Privacidad│ ✅ SÍ se justifica en escenario Expansión│
│ • Cero latencia en autocompletado y agentes locales.                  │
│ • Privacidad total de código industrial y datos de clientes.           │
│ • Procesamiento local de series temporales de medidores de energía.   │
└──────────────────────────────┴─────────────────────────────────────────┘
```

### Directrices para la GPU:
1. **No sobre-endeudarse en GPU de gama extrema:** No solicitar un crédito elevado para comprar una RTX 4090 o hardware enterprise.
2. **Recomendación Óptima:**
   * **Opción Económica:** *Nvidia RTX 3060 12GB VRAM* (Permite correr modelos Qwen2.5-Coder 7B/14B cuantizados y embeddings locales con fluidez absoluta).
   * **Opción Avanzada:** *Nvidia RTX 4060 Ti 16GB VRAM* (Mayor ancho de banda y capacidad para modelos de 14B/32B cuantizados con contexto amplio).
3. **Prioridad Relativa:** La indumentaria y el marketing digital tienen **prioridad 1** porque generan dinero entrante directo; la GPU es una inversión de **eficiencia y aceleración de desarrollo** (prioridad 2).
