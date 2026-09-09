"""Servicio de cálculo de presupuestos modulares (WBS) y motor de pricing en ARS."""

import os
from typing import Any, cast

import yaml

from src.application.dtos.pricing_dto import (
    CalculoPaybackDTO,
    ItemDescuentoDTO,
    LineasRemotasDTO,
    PresupuestoCalculadoDTO,
    SubitemPresupuestoDTO,
    TarifaConsultoriaDTO,
)


class PricingService:
    """Servicio de aplicación para presupuestación modular y control de pricing."""

    def __init__(self, data_dir: str | None = None) -> None:
        if not data_dir or (data_dir == "data" and "DATA_DIR" in os.environ):
            self.data_dir = os.getenv("DATA_DIR", "data")
        else:
            self.data_dir = data_dir
        self.pricing_path: str = os.path.join(self.data_dir, "content", "pricing_structure.yaml")
        self._cached_config: dict[str, Any] | None = None

    def get_config(self) -> dict[str, Any]:
        """Carga y cachea la configuración de pricing desde YAML."""
        if self._cached_config is None:
            if not os.path.exists(self.pricing_path):
                return {
                    "config": {"currency": "ARS", "show_public_prices": False},
                    "viaticos_zonas": {"base_general_gba_norte_ars": 50000},
                    "wbs_subitems": {},
                    "relevamiento_inicial": {"diagnostico_base_ars": 55000},
                    "descuentos": {"bapro_pct": 0.10, "vitrina_pct": 0.15, "stacking_max_pct": 0.25},
                    "consultoria_escalonada": {},
                    "servicios_remotos": {},
                }
            with open(self.pricing_path, encoding="utf-8") as f:
                raw_loaded: Any = yaml.safe_load(f)
                raw_data: dict[str, Any] = cast(dict[str, Any], raw_loaded or {})
            self._cached_config = raw_data
        return self._cached_config

    def is_public_pricing_enabled(self) -> bool:
        """Verifica si la variable booleana de precios públicos está activa."""
        cfg: dict[str, Any] = cast(dict[str, Any], self.get_config().get("config", {}))
        return bool(cfg.get("show_public_prices", False))

    def resolver_viaticos(self, cp: str | None = None) -> tuple[float, str]:
        """Resuelve el importe de viáticos y la denominación de la zona por Código Postal."""
        config = self.get_config()
        zonas: dict[str, Any] = cast(dict[str, Any], config.get("viaticos_zonas", {}))
        base_general: float = float(zonas.get("base_general_gba_norte_ars", 50000))

        if not cp:
            return base_general, "Zona Norte GBA (Base)"

        cp_clean = str(cp).strip()
        for clave, val in zonas.items():
            if isinstance(val, dict):
                data: dict[str, Any] = cast(dict[str, Any], val)
                if "cp_list" in data:
                    raw_list: list[Any] = cast(list[Any], data.get("cp_list", []))
                    cp_list: list[str] = [str(c).strip() for c in raw_list]
                    if cp_clean in cp_list:
                        tarifa: float = float(data.get("tarifa_ars", base_general))
                        nombre: str = str(data.get("nombre", clave))
                        return tarifa, nombre

        return base_general, f"Zona GBA (CP {cp_clean})"

    def calcular_presupuesto_obra(
        self,
        codigos_subitems: list[str] | None = None,
        cp: str | None = None,
        tiene_convenio_bapro: bool = False,
        adhiere_vitrina_publica: bool = False,
        aplico_diagnostico_previo: bool = False,
    ) -> PresupuestoCalculadoDTO:
        """Calcula el presupuesto modular sumando sub-ítems, viáticos, deducciones y descuentos."""
        config = self.get_config()
        wbs_defs: dict[str, Any] = cast(dict[str, Any], config.get("wbs_subitems", {}))
        descuentos_root = config.get("descuentos")
        cfg_dict: dict[str, Any] = cast(dict[str, Any], config.get("config", {}))
        descuentos_cfg: dict[str, Any] = cast(dict[str, Any], descuentos_root or cfg_dict.get("descuentos", {}))
        relev_cfg: dict[str, Any] = cast(dict[str, Any], config.get("relevamiento_inicial", {}))

        # Sub-ítems por defecto: Instalación estándar (b) + Puesta en marcha cloud (e)
        seleccionados_codigos: set[str] = set(codigos_subitems or ["b", "e"])

        # 1. Viáticos
        viaticos_monto, zona_nombre = self.resolver_viaticos(cp)

        # 2. Sub-ítems de mano de obra
        lista_subitems: list[SubitemPresupuestoDTO] = []
        subtotal_mano_obra: float = 0.0

        for key, item_val in wbs_defs.items():
            if not isinstance(item_val, dict):
                continue
            item_data: dict[str, Any] = cast(dict[str, Any], item_val)
            cod: str = str(item_data.get("codigo", ""))
            # El código "a" representa viáticos que se computan por separado
            if cod == "a":
                continue
            tarifa: float = float(item_data.get("tarifa_ars", 0.0))
            activo: bool = cod in seleccionados_codigos
            nom: str = str(item_data.get("nombre", key))
            desc: str = str(item_data.get("descripcion", ""))
            dto = SubitemPresupuestoDTO(
                codigo=cod,
                nombre=nom,
                descripcion=desc,
                tarifa_ars=tarifa,
                seleccionado=activo,
            )
            if activo:
                subtotal_mano_obra += tarifa
                lista_subitems.append(dto)

        subtotal_bruto: float = viaticos_monto + subtotal_mano_obra

        # 3. Descuentos comerciales (Stacking)
        bapro_pct: float = float(descuentos_cfg.get("bapro_pct", 0.10))
        vitrina_pct: float = float(descuentos_cfg.get("vitrina_pct", 0.15))
        max_pct: float = float(descuentos_cfg.get("stacking_max_pct", 0.25))

        descuentos_aplicados: list[ItemDescuentoDTO] = []
        pct_total: float = 0.0

        if tiene_convenio_bapro and adhiere_vitrina_publica:
            pct_total = min(bapro_pct + vitrina_pct, max_pct)
            monto_desc = subtotal_bruto * pct_total
            descuentos_aplicados.append(
                ItemDescuentoDTO(
                    concepto=f"Stacking Total BAPRO ({int(bapro_pct * 100)}%) + Vitrina ({int(vitrina_pct * 100)}%)",
                    porcentaje=pct_total,
                    monto_ars=monto_desc,
                )
            )
        elif tiene_convenio_bapro:
            pct_total = bapro_pct
            monto_desc = subtotal_bruto * pct_total
            descuentos_aplicados.append(
                ItemDescuentoDTO(
                    concepto=f"Descuento Comercial Banco Provincia ({int(bapro_pct * 100)}% OFF)",
                    porcentaje=pct_total,
                    monto_ars=monto_desc,
                )
            )
        elif adhiere_vitrina_publica:
            pct_total = vitrina_pct
            monto_desc = subtotal_bruto * pct_total
            descuentos_aplicados.append(
                ItemDescuentoDTO(
                    concepto=f"Bonificación Programa Vitrina Pública ({int(vitrina_pct * 100)}% OFF)",
                    porcentaje=pct_total,
                    monto_ars=monto_desc,
                )
            )

        total_descuentos: float = sum(d.monto_ars for d in descuentos_aplicados)

        # 4. Deducción de relevamiento inicial
        diag_bonificado: float = 0.0
        if aplico_diagnostico_previo:
            diag_bonificado = float(relev_cfg.get("diagnostico_base_ars", 55000))

        total_neto: float = max(0.0, subtotal_bruto - total_descuentos - diag_bonificado)
        ahorro_total: float = total_descuentos + diag_bonificado

        # 5. Generación de texto para WhatsApp
        resumen_wa: str = self._generar_resumen_whatsapp(
            subitems=lista_subitems,
            zona_nombre=zona_nombre,
            viaticos=viaticos_monto,
            subtotal_bruto=subtotal_bruto,
            descuentos=descuentos_aplicados,
            diag_bonificado=diag_bonificado,
            total_neto=total_neto,
            ahorro_total=ahorro_total,
        )

        resumen_formal: str = self._generar_resumen_formal(
            subitems=lista_subitems,
            zona_nombre=zona_nombre,
            viaticos=viaticos_monto,
            subtotal_bruto=subtotal_bruto,
            descuentos=descuentos_aplicados,
            diag_bonificado=diag_bonificado,
            total_neto=total_neto,
        )

        return PresupuestoCalculadoDTO(
            zona_nombre=zona_nombre,
            cp_destino=cp,
            subitems=lista_subitems,
            subtotal_mano_obra_ars=subtotal_mano_obra,
            viaticos_ars=viaticos_monto,
            subtotal_bruto_ars=subtotal_bruto,
            descuentos_aplicados=descuentos_aplicados,
            total_descuentos_ars=total_descuentos,
            diagnostico_previo_bonificado_ars=diag_bonificado,
            total_neto_ars=total_neto,
            ahorro_total_ars=ahorro_total,
            resumen_whatsapp=resumen_wa,
            resumen_texto_formal=resumen_formal,
        )

    def obtener_tarifas_consultoria(self) -> list[TarifaConsultoriaDTO]:
        """Retorna el listado tipado de tarifas escalonadas de consultoría (C-12)."""
        config = self.get_config()
        consultoria_raw: dict[str, Any] = cast(dict[str, Any], config.get("consultoria_escalonada", {}))
        resultado: list[TarifaConsultoriaDTO] = []
        for _key, val in consultoria_raw.items():
            if isinstance(val, dict):
                item_data: dict[str, Any] = cast(dict[str, Any], val)
                if "categoria" in item_data and "tarifa_base_ars" in item_data:
                    resultado.append(
                        TarifaConsultoriaDTO(
                            categoria=str(item_data.get("categoria", "")),
                            rango=str(item_data.get("rango", "")),
                            tarifa_base_ars=float(item_data.get("tarifa_base_ars", 0.0)),
                            descripcion=str(item_data.get("descripcion", "")),
                        )
                    )
        return resultado

    def obtener_lineas_remotas(self) -> LineasRemotasDTO:
        """Retorna las tarifas tipadas para servicios remotos y MRR DataMaq Insights."""
        config = self.get_config()
        remotos_raw: dict[str, Any] = cast(dict[str, Any], config.get("servicios_remotos", {}))
        tele_peritaje: dict[str, Any] = cast(dict[str, Any], remotos_raw.get("tele_peritaje_documental", {}))
        in_company: dict[str, Any] = cast(dict[str, Any], remotos_raw.get("capacitacion_in_company_virtual", {}))
        insights: dict[str, Any] = cast(dict[str, Any], remotos_raw.get("datamaq_insights_mrr", {}))

        return LineasRemotasDTO(
            tele_peritaje_ars=float(tele_peritaje.get("tarifa_ars", 150000.0)),
            capacitacion_in_company_ars=float(in_company.get("tarifa_ars", 450000.0)),
            datamaq_insights_min_ars=float(insights.get("tarifa_min_ars", 85000.0)),
            datamaq_insights_max_ars=float(insights.get("tarifa_max_ars", 150000.0)),
        )

    def calcular_payback(
        self,
        categoria_tarifa: str,
        perdida_mensual_ars: float,
        inversion_total_ars: float,
    ) -> CalculoPaybackDTO:
        """Calcula el retorno de inversión (Payback en días y meses) y genera el resumen para CFO."""
        if perdida_mensual_ars <= 0:
            raise ValueError("La pérdida mensual debe ser mayor a 0 ARS")
        if inversion_total_ars <= 0:
            raise ValueError("La inversión total debe ser mayor a 0 ARS")

        meses_payback = round(inversion_total_ars / perdida_mensual_ars, 1)
        dias_payback = max(1, round((inversion_total_ars / perdida_mensual_ars) * 30))
        ahorro_anual_proyectado = (perdida_mensual_ars * 12) - inversion_total_ars

        resumen_cfo = (
            f"📊 INFORME EJECUTIVO DE RETORNO DE INVERSIÓN (PAYBACK) — Tarifa {categoria_tarifa}\n"
            f"• Penalidad/Pérdida Mensual Actual: ${int(perdida_mensual_ars):,} ARS\n"
            f"• Inversión Integral DataMaq (Hardware + Obra + Consultoría): ${int(inversion_total_ars):,} ARS\n"
            f"• Período de Recuperación (Payback): {dias_payback} días (~{meses_payback} meses)\n"
            f"• Ahorro Neto Proyectado a 12 meses: ${int(ahorro_anual_proyectado):,} ARS\n"
            f"• Conclusión Financiera: Inversión de alta eficiencia con repago acelerado financiable en cuotas con Pactar Digital."
        ).replace(",", ".")

        return CalculoPaybackDTO(
            categoria_tarifa=categoria_tarifa,
            perdida_mensual_estimada_ars=perdida_mensual_ars,
            inversion_total_ars=inversion_total_ars,
            dias_payback=dias_payback,
            meses_payback=meses_payback,
            ahorro_anual_proyectado_ars=ahorro_anual_proyectado,
            resumen_ejecutivo_cfo=resumen_cfo,
        )

    def get_plan_display_price(self, plan_id: str, default_price: str = "A cotizar") -> str:
        """Devuelve el precio formateado según la bandera booleana show_public_prices."""
        if plan_id == "plataforma-cloud":
            return "$0"

        if not self.is_public_pricing_enabled():
            return default_price

        config = self.get_config()
        referencias: dict[str, Any] = cast(dict[str, Any], config.get("planes_referencia_publica", {}))
        plan_ref: dict[str, Any] = cast(dict[str, Any], referencias.get(plan_id, {}))
        precio_num = plan_ref.get("precio_base_ars")

        if precio_num is not None:
            return f"${int(precio_num):,}".replace(",", ".")

        return default_price

    def _generar_resumen_whatsapp(
        self,
        subitems: list[SubitemPresupuestoDTO],
        zona_nombre: str,
        viaticos: float,
        subtotal_bruto: float,
        descuentos: list[ItemDescuentoDTO],
        diag_bonificado: float,
        total_neto: float,
        ahorro_total: float,
    ) -> str:
        lineas: list[str] = [
            "⚡ *DATAMAQ — Presupuesto Estimado de Instalación*",
            "Ingeniería de datos: de la planta a la oficina.",
            "━━━━━━━━━━━━━━━━━━━━━",
            f"📍 *Zona / Logística:* {zona_nombre} (${int(viaticos):,})".replace(",", "."),
            "",
            "🛠️ *Alcance de Obra en Tablero:*",
        ]

        for s in subitems:
            lineas.append(f" • {s.nombre}: ${int(s.tarifa_ars):,}".replace(",", "."))

        lineas.append("")
        lineas.append(f"📊 *Subtotal Bruto:* ${int(subtotal_bruto):,}".replace(",", "."))

        if descuentos:
            for d in descuentos:
                lineas.append(f"🎁 *{d.concepto}:* -${int(d.monto_ars):,}".replace(",", "."))

        if diag_bonificado > 0:
            lineas.append(f"✅ *Peritaje Inicial Deducible (100%):* -${int(diag_bonificado):,}".replace(",", "."))

        lineas.append("━━━━━━━━━━━━━━━━━━━━━")
        lineas.append(f"💰 *TOTAL NETO ESTIMADO:* ${int(total_neto):,} ARS".replace(",", "."))

        if ahorro_total > 0:
            lineas.append(f"🎉 *Ahorro Total Aplicado:* ${int(ahorro_total):,} ARS".replace(",", "."))

        lineas.append("")
        lineas.append("🔒 *Condiciones y Garantía:*")
        lineas.append("• Póliza AP/ART al día en Federación Patronal Seguros.")
        lineas.append("• Hardware por compra directa a Powermeter SAS a precio de lista.")
        lineas.append("• Financiación en cuotas productivas disponible con Pactar Digital.")
        lineas.append("• Entrega formal con Acta de Puesta en Marcha y enlace a plataforma $0.")

        return "\n".join(lineas)

    def _generar_resumen_formal(
        self,
        subitems: list[SubitemPresupuestoDTO],
        zona_nombre: str,
        viaticos: float,
        subtotal_bruto: float,
        descuentos: list[ItemDescuentoDTO],
        diag_bonificado: float,
        total_neto: float,
    ) -> str:
        lineas: list[str] = [
            "PROPUESTA COMERCIAL Y PRESUPUESTO TÉCNICO",
            "GRUPO DATAMAQ — Servicios de Ingeniería y Telemetría en Baja Tensión",
            "=" * 60,
            f"Zona de Intervención: {zona_nombre}",
            f"Viáticos y Traslado Operativo: ${int(viaticos):,} ARS".replace(",", "."),
            "",
            "DETALLE DE MANO DE OBRA Y SERVICIOS TÉCNICOS (WBS):",
        ]
        for s in subitems:
            lineas.append(f"  [{s.codigo}] {s.nombre}: ${int(s.tarifa_ars):,} ARS".replace(",", "."))

        lineas.append("-" * 60)
        lineas.append(f"Subtotal Bruto: ${int(subtotal_bruto):,} ARS".replace(",", "."))

        for d in descuentos:
            lineas.append(f"Bonificación ({d.concepto}): -${int(d.monto_ars):,} ARS".replace(",", "."))

        if diag_bonificado > 0:
            lineas.append(f"Crédito Peritaje Inicial Deducible: -${int(diag_bonificado):,} ARS".replace(",", "."))

        lineas.append("=" * 60)
        lineas.append(f"TOTAL FINAL PROPUESTA: ${int(total_neto):,} ARS".replace(",", "."))
        return "\n".join(lineas)
