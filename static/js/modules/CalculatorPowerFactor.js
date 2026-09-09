/**
 * @fileoverview Calculadora interactiva de compensación reactiva y penalidades de factor de potencia (Res. ENRE 544/2024).
 * Permite estimar en tiempo real los kVAR requeridos de banco de capacitores y actualiza dinámicamente el CTA de WhatsApp.
 */

export class CalculatorPowerFactor {
    /**
     * @param {HTMLElement} container - Contenedor raíz de la calculadora.
     * @param {string} [phone="541156297160"] - Número de WhatsApp de DataMaq.
     */
    constructor(container, phone = "541156297160") {
        /** @type {HTMLElement} */
        this.container = container;
        /** @type {string} */
        this.phone = phone;

        /** @type {HTMLInputElement | null} */
        this.kwInput = container.querySelector("#calc-kw");
        /** @type {HTMLInputElement | HTMLSelectElement | null} */
        this.cosPhiInput = container.querySelector("#calc-cos-phi");
        /** @type {HTMLElement | null} */
        this.resultKvar = container.querySelector("#calc-result-kvar");
        /** @type {HTMLElement | null} */
        this.statusBadge = container.querySelector("#calc-status-badge");
        /** @type {HTMLElement | null} */
        this.statusDesc = container.querySelector("#calc-status-desc");
        /** @type {HTMLAnchorElement | null} */
        this.ctaWhatsApp = container.querySelector("#calc-cta-whatsapp");

        this.init();
    }

    /**
     * Inicializa los escuchadores de eventos para actualización en tiempo real.
     * @returns {void}
     */
    init() {
        if (this.kwInput) {
            this.kwInput.addEventListener("input", () => this.calculate());
            this.kwInput.addEventListener("change", () => this.calculate());
        }
        if (this.cosPhiInput) {
            this.cosPhiInput.addEventListener("input", () => this.calculate());
            this.cosPhiInput.addEventListener("change", () => this.calculate());
        }
        this.calculate();
    }

    /**
     * Realiza el cálculo trigonométrico normativo y actualiza el DOM.
     * @returns {void}
     */
    calculate() {
        const kw = Math.max(1, parseFloat(this.kwInput?.value || "50") || 50);
        const cosPhi = Math.min(0.99, Math.max(0.40, parseFloat(this.cosPhiInput?.value || "0.78") || 0.78));
        const targetCosPhi = 0.96;

        let kvarRequired = 0;
        if (cosPhi < targetCosPhi) {
            const phi1 = Math.acos(cosPhi);
            const phi2 = Math.acos(targetCosPhi);
            const q = kw * (Math.tan(phi1) - Math.tan(phi2));
            kvarRequired = Math.max(0, Math.round(q));
        }

        // Actualizar valor numérico de kVAR
        if (this.resultKvar) {
            this.resultKvar.textContent = `${kvarRequired} kVAR`;
        }

        // Clasificación de severidad según Res. ENRE 544/2024
        let badgeText = "Normalizado";
        let badgeClass = "tw:bg-green-900/40 tw:text-green-300 tw:border-green-700/50";
        let descText = "Cumple con el límite de cos φ ≥ 0,95 de la Res. ENRE 544/2024. Sin recargos por reactiva.";

        if (cosPhi < 0.60) {
            badgeText = "⚠️ Riesgo de Corte (Art. 9)";
            badgeClass = "tw:bg-red-900/50 tw:text-red-300 tw:border-red-600";
            descText = `Penalidad crítica severa. La distribuidora está habilitada por el Art. 9 de la Res. ENRE 544/2024 a intimar y suspender el suministro eléctrico. Requiere banco de aprox. ${kvarRequired} kVAR urgente.`;
        } else if (cosPhi < 0.85) {
            badgeText = "❌ Penalidad Severa";
            badgeClass = "tw:bg-red-900/40 tw:text-red-300 tw:border-red-700/50";
            descText = `Recargo mensual significativo en energía y potencia. Se aconseja instalar analizador SmartPlus y banco de aprox. ${kvarRequired} kVAR.`;
        } else if (cosPhi < 0.95) {
            badgeText = "⚠️ Fuera de Norma ENRE";
            badgeClass = "tw:bg-amber-900/40 tw:text-amber-300 tw:border-amber-700/50";
            descText = `Incumple el nuevo límite de cos φ ≥ 0,95. Genera recargos mensuales automáticos en la factura. Compensación sugerida: ${kvarRequired} kVAR.`;
        }

        if (this.statusBadge) {
            this.statusBadge.textContent = badgeText;
            this.statusBadge.className = `tw:px-3 tw:py-1 tw:rounded-full tw:text-xs tw:font-semibold tw:border ${badgeClass}`;
        }

        if (this.statusDesc) {
            this.statusDesc.textContent = descText;
        }

        // Actualizar CTA dinámico a WhatsApp
        if (this.ctaWhatsApp) {
            const msg = `Hola! Calculé en su web una compensación de ${kvarRequired} kVAR para una potencia de ${kw} kW (cos φ actual ${cosPhi.toFixed(2)}) y necesito cotización para normalizar mi suministro.`;
            this.ctaWhatsApp.href = `https://wa.me/${this.phone}?text=${encodeURIComponent(msg)}`;
        }
    }
}
