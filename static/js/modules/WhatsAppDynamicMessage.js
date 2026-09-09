/**
 * @fileoverview Módulo de Mensajes Dinámicos de WhatsApp para Campañas SEM y Atribución.
 * Captura parámetros UTM/gclid/fbclid/li_fat_id, los persiste durante la sesión
 * y actualiza dinámicamente los atributos href de los enlaces wa.me con mensajes contextualizados.
 */

import { warn as logWarn } from './logger.js';

/**
 * Clave de almacenamiento de sesión para los datos de campaña de WhatsApp.
 * @type {string}
 */
const STORAGE_KEY = 'dm_whatsapp_campaign_data';

/**
 * Tabla de equivalencias de mensajes para campañas SEM conocidas de DataMaq.
 * @type {Record<string, string>}
 */
const CAMPAIGN_MAPPING = {
    'mantenimiento-amba': 'Vi el anuncio de Mantenimiento Eléctrico e Industrial en AMBA y quiero más información',
    'mantenimiento-industrial': 'Vi el anuncio de Mantenimiento Eléctrico Industrial y quiero solicitar una inspección',
    'calidad-energia': 'Tengo una penalidad de factor de potencia en la factura eléctrica y necesito presupuesto para un banco de capacitores.',
    'telemetria-industrial': 'Me interesa digitalizar máquinas con telemetría industrial Powermeter sin cambiar mis PLCs.',
    'retrofit-iot': 'Vi el anuncio de Retrofit IoT y Automatización con Powermeter y quiero más información',
    'integracion-xubio': 'Vi el anuncio de Integración de Datos a Xubio y quiero asesoramiento',
    'habilitaciones-electricas': 'Vi el anuncio de Habilitaciones y Mediciones Eléctricas SRT 3068 y quiero asesoramiento'
};

/**
 * Captura y persiste los datos de campaña publicitarios presentes en la URL actual.
 * Si no existen parámetros en la URL, intenta recuperar los datos almacenados previamente en la sesión.
 *
 * @returns {import('../types.js').CampaignData | null} Objeto con los datos de campaña capturados o null si no existen.
 */
export function captureAndPersistCampaign() {
    try {
        const urlParams = new URLSearchParams(window.location.search);
        const utmCampaign = urlParams.get('utm_campaign')?.trim();
        const utmSource = urlParams.get('utm_source')?.trim()?.toLowerCase();
        const utmMedium = urlParams.get('utm_medium')?.trim()?.toLowerCase();
        const gclid = urlParams.get('gclid') || urlParams.get('wbraid') || urlParams.get('gbraid');
        const fbclid = urlParams.get('fbclid');
        const liFatId = urlParams.get('li_fat_id');

        const hasCampaignParams = utmCampaign || gclid || fbclid || liFatId || utmSource;

        if (hasCampaignParams) {
            /** @type {import('../types.js').CampaignData} */
            const data = {
                utmCampaign: utmCampaign || null,
                utmSource: utmSource || null,
                utmMedium: utmMedium || null,
                gclid: gclid || null,
                fbclid: fbclid || null,
                liFatId: liFatId || null,
                timestamp: Date.now()
            };
            sessionStorage.setItem(STORAGE_KEY, JSON.stringify(data));
            return data;
        }

        // Si no hay parámetros en la URL actual, intentar recuperar de sessionStorage
        const cached = sessionStorage.getItem(STORAGE_KEY);
        if (cached) {
            return JSON.parse(cached);
        }
    } catch (e) {
        logWarn("[WhatsAppDynamicMessage] No se pudo acceder a sessionStorage:", e);
    }

    return null;
}

/**
 * Formatea automáticamente cualquier slug de campaña desconocido.
 * Reemplaza guiones y guiones bajos por espacios y capitaliza cada término.
 *
 * @param {string | null | undefined} slug - Nombre técnico o slug de la campaña.
 * @returns {string} Nombre formateado en formato título legible.
 */
function formatCampaignName(slug) {
    if (!slug) return '';
    return slug
        .replace(/[-_]+/g, ' ')
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
        .join(' ');
}

/**
 * Genera el texto del mensaje dinámico personalizado para iniciar la conversación por WhatsApp.
 *
 * @param {string} [defaultMessage='Hola! Vi tu sitio datamaq.com.ar y quería consultarte sobre servicios de mantenimiento eléctrico industrial.'] - Mensaje predeterminado de respaldo.
 * @returns {string} Mensaje final a inyectar en el query param `text` del enlace de WhatsApp.
 */
export function buildDynamicWhatsAppMessage(defaultMessage = 'Hola! Vi tu sitio datamaq.com.ar y quería consultarte sobre servicios de mantenimiento eléctrico industrial.') {
    const campaignData = captureAndPersistCampaign();

    if (!campaignData) {
        return defaultMessage;
    }

    const { utmCampaign, utmSource, gclid, fbclid, liFatId } = campaignData;

    // 1. Coincidencia exacta en tabla de campañas
    if (utmCampaign && CAMPAIGN_MAPPING[utmCampaign.toLowerCase()]) {
        return `Hola! ${CAMPAIGN_MAPPING[utmCampaign.toLowerCase()]}`;
    }

    // 2. Campaña con formateo inteligente automático
    if (utmCampaign) {
        const formatted = formatCampaignName(utmCampaign);
        return `Hola! Vi el anuncio de ${formatted} y quiero más información.`;
    }

    // 3. Fallbacks por plataforma pagada sin utm_campaign explícito
    if (gclid || utmSource === 'google' || utmSource === 'google_ads') {
        return 'Hola! Vi su anuncio en Google y quiero pedir más información.';
    }
    if (fbclid || utmSource === 'facebook' || utmSource === 'instagram' || utmSource === 'meta') {
        return 'Hola! Vi su anuncio en redes sociales y quiero pedir más información.';
    }
    if (liFatId || utmSource === 'linkedin') {
        return 'Hola! Vi su anuncio en LinkedIn y me gustaría solicitar información sobre sus servicios.';
    }

    return defaultMessage;
}

/**
 * Actualiza todos los enlaces de WhatsApp (a[href*="wa.me"] y .c-whatsapp-fab) presentes en el DOM.
 *
 * @param {string} [phone='541156297160'] - Número telefónico de WhatsApp de DataMaq con código de país.
 * @returns {void}
 */
export function updateWhatsAppLinks(phone = '541156297160') {
    const message = buildDynamicWhatsAppMessage();
    const encodedMessage = encodeURIComponent(message);
    const targetUrl = `https://wa.me/${phone}?text=${encodedMessage}`;

    /** @type {NodeListOf<HTMLAnchorElement>} */
    const whatsappElements = document.querySelectorAll('a[href*="wa.me"], .c-whatsapp-fab');
    whatsappElements.forEach((el) => {
        el.setAttribute('href', targetUrl);
    });
}
