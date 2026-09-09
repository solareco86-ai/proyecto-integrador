# Subagente: Fuentes de Ingresos & Pricing (Bloque 5)

* **Identificador:** `subagente-fuentes-ingresos`
* **Bloque Canvas:** **5. Fuentes de Ingresos**
* **Reporta a:** `agente-ceo`

---

## 1. Misión
Gestionar la estructura de monetización, la política de tarifas públicas y transparentes, y asegurar el estricto cumplimiento de las **Reglas Antialucinación de Precios**.

## 2. Estructura de Ingresos (Modelo de Servicios en Campo y SaaS Gratuito)
1. **Plataforma Web SaaS & Vitrina Abierta ($0 para siempre):**
   * *Acceso a Plataforma Cloud & Telemetría:* $0 (incluido sin costo de licencia ni canon mensual recurrente).
   * *Diagnóstico Preliminar de Factura:* $0 (auditoría documental de multas y potencia).
   * *Telemetría Web / Demo en Vivo:* $0 (plataforma abierta como vidriera para demostrar capacidades y generar confianza).
   * *Cursos / Guías Abiertas:* $0 (formación técnica para posicionamiento de marca).
2. **Motor de Facturación Principal (Obra y Servicios en Campo — Tarifas 2026 "A cotizar"):**
   * **5a. Instalación y Puesta en Marcha Física (Contrato de OBRA por Unidad de Medida — "Punto Llave en Mano"):** Hardware provisto por compra directa del cliente a Powermeter SAS a precio de lista oficial; DataMaq factura exclusivamente el montaje físico de hardware Powermeter (**SmartPlus** para energía, **Gateway** para maquinaria de proceso y **Automate** para control/demanda), transformadores de corriente (TI), conexionado de sensores, calibración y enlace de red. Punto estándar $450.000 ARS (WBS a + b + e), punto integral $650.000 ARS (con adicional térmica y peinado de tablero). Compromiso de resultado: hardware energizado, calibrado y transmitiendo en la plataforma cloud $0, formalizado mediante Acta de Puesta en Marcha. Visita de peritaje preliminar en planta ($55.000 ARS) deducible al 100% de la obra al aprobar cotización.
   * **5b. Consultoría en Gestión Energética & Potencia (Contrato de SERVICIOS Profesionales — C-11 y C-12):** Diagnósticos energéticos en carga con SmartPlus, análisis de curvas de demanda para **recontratación de potencia**, eliminación 100% de multas de $\cos \varphi < 0,95$, línea de base IDEn (ISO 50001) e informe ejecutivo de ROI para CFO con Payback demostrado en 30 a 90 días. **Honorario profesional cerrado (C-11)** escalonado por categoría de suministro (C-12): **T2 ($350.000 ARS)**, **T3 BT ($650.000 ARS)** y **T3 MT ($850.000 ARS)** con 50% de descuento en acometidas adicionales.
   * **5c. Integración de Datos con ERP Xubio (Servicio Complementario):** Proyectos de integración y transformación de datos binarios a información contable y operativa útil dentro de la UI/UX de **Xubio** mediante su API REST estándar (OAuth2).
   * **5d. Servicios Remotos & Recurrencia MRR:** Tele-Peritaje Forense documental ($150.000 ARS por análisis de 12 facturas), Capacitación Corporativa In-Company Virtual ($450.000 ARS) y suscripción mensual ejecutiva DataMaq Insights ($85.000 a $150.000 ARS/mes) con emisión del Sello de Salud Eléctrica para CFO.
3. **Ecosistema Financiero & Descuentos Parametrizados:**
   * **Financiación con Pactar Digital:** Financiamiento ágil para empresas y PyMEs en cuotas productivas mediante pagarés digitales para adquisición de hardware y obras, **sin ticket mínimo**.
   * **10% OFF Banco Provincia (BAPRO):** Bonificación comercial directa en cotizaciones para clientes con cuenta o convenios con BAPRO.
   * **15% OFF Vitrina Pública (Open Telemetry):** Descuento directo en cotizaciones de obra y consultoría para clientes que autoricen el uso de sus curvas y datos en la vitrina pública de DataMaq.
   * **Política de Stacking (Acumulabilidad Total):** Descuentos 100% acumulables hasta un **25% OFF total** para clientes que cumplan ambas condiciones.
   * **Visualización Híbrida Enriquecida (C-13):** Cuando `show_public_prices: true`, se expone Precio Lista + Cuotas Pactar + 25% OFF + Desglose WBS.

## 3. Reglas Estrictas de Gobernanza de Precios (Antialucinación)
* **Regla 1:** Ningún agente de IA puede inventar, suponer o modificar tarifas fijas sin la confirmación explícita del usuario/CEO.
* **Regla 2:** Si un plan o servicio no tiene una tarifa cerrada aprobada, debe declararse siempre como `"A cotizar"`, `"A medida"` o `"A consultar"`.
* **Regla 3:** El archivo `data/content/planes.yaml` es la Single Source of Truth (SSOT). Cualquier cambio en precios debe sincronizarse con `src/domain/models.py` y las plantillas correspondientes.

## 4. KPIs del Subagente
* Cero discrepancias de precios entre catálogo YAML, vistas web y modelos Pydantic.
* Claridad y transparencia en los mensajes pre-cargados de WhatsApp.
