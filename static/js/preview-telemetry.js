/**
 * @fileoverview Script de telemetría responsive e informe UI/UX para auditoría en desarrollo.
 * Se activa únicamente cuando la URL contiene el parámetro ?telemetry=1.
 */

(function() {
    // Desactivar el borrado y ruido de consola salvo que se especifique ?telemetry=1 en la URL
    if (!window.location.search.includes('telemetry=1')) return;

    setTimeout(() => {
        reportResponsive();
    }, 1000);

    window.addEventListener('resize', () => {
        reportResponsive();
    });

    /**
     * Evalúa el layout de la página y reporta métricas responsive en la consola del navegador.
     * @returns {void}
     */
    function reportResponsive() {
        const footer = document.querySelector('footer');
        const rect = footer ? footer.getBoundingClientRect() : null;
        
        /** @type {Array<{etiqueta: string, clase: string, ancho_contenido_px: number, ancho_visible_px: number, extracto: string}>} */
        const overflows = [];
        document.querySelectorAll('*').forEach(el => {
            if (el.scrollWidth > el.clientWidth && el.clientWidth > 0) {
                const computed = window.getComputedStyle(el);
                if (computed.overflowX !== 'auto' && computed.overflowX !== 'scroll') {
                    overflows.push({
                        etiqueta: el.tagName,
                        clase: el.className || 'Sin clase',
                        ancho_contenido_px: el.scrollWidth,
                        ancho_visible_px: el.clientWidth,
                        extracto: (el.textContent || '').trim().substring(0, 30)
                    });
                }
            }
        });

        const links = Array.from(document.querySelectorAll('a'));
        const touchTargets = links.map(a => {
            const r = a.getBoundingClientRect();
            return {
                label: (a.textContent || '').trim().substring(0, 15),
                alto_px: Math.round(r.height),
                ancho_px: Math.round(r.width)
            };
        });
        const targetIssues = touchTargets.filter(t => t.alto_px > 0 && t.alto_px < 32);

        const info = {
            ruta_actual: window.location.pathname,
            ancho_viewport_px: window.innerWidth,
            alto_viewport_px: window.innerHeight,
            ancho_scroll_body_px: document.body.scrollWidth,
            elementos_con_desbordamiento_horizontal: overflows,
            medidas_footer: rect ? {
                ancho_px: Math.round(rect.width),
                alto_px: Math.round(rect.height)
            } : 'No renderizado',
            UX_enlaces: {
                total_enlaces_pagina: links.length,
                enlaces_con_area_pequena: targetIssues.length,
                listado_alertas_click: targetIssues.slice(0, 5)
            }
        };

        console.log("%c📱 TELEMETRÍA RESPONSIVE E INFORME UI/UX:", "color: #ff9f43; font-weight: bold; font-size: 14px;");
        console.log(JSON.stringify(info, null, 2));
    }
})();
