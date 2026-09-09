/**
 * @fileoverview Módulo de Atribución de Tráfico (First-Touch Attribution B2B).
 * Analiza parámetros UTM, Google Ads (gclid, gbraid, wbraid), Referrers y Redes Sociales
 * para clasificar el origen del prospecto y persistirlo durante 30 días en localStorage
 * y en sessionStorage para la sesión actual.
 */

/**
 * Clave de almacenamiento de sesión para la atribución de tráfico.
 * @type {string}
 */
const SESSION_STORAGE_KEY = 'dm_traffic_source';

/**
 * Clave de almacenamiento local persistente (ventana de 30 días).
 * @type {string}
 */
const LOCAL_STORAGE_KEY = 'dm_attribution_v1';

/**
 * Ventana de vigencia para atribución B2B (30 días en milisegundos).
 * @type {number}
 */
const ATTRIBUTION_WINDOW_MS = 30 * 24 * 60 * 60 * 1000;

/**
 * Recupera el registro persistente de atribución si aún está vigente.
 * @returns {import('../types.js').AttributionRecord | null}
 */
export function getAttributionRecord() {
    try {
        const raw = localStorage.getItem(LOCAL_STORAGE_KEY);
        if (!raw) return null;
        /** @type {import('../types.js').AttributionRecord} */
        const parsed = JSON.parse(raw);
        if (parsed && typeof parsed.timestamp === 'number' && (Date.now() - parsed.timestamp < ATTRIBUTION_WINDOW_MS)) {
            return parsed;
        }
    } catch (_) {}
    return null;
}

/**
 * Obtiene la fuente de atribución first-touch del visitante.
 * Prioriza parámetros activos en URL (nueva campaña), luego atribución de sesión,
 * luego atribución persistida en localStorage (30 días) y finalmente evalúa referrer.
 *
 * @returns {string} Texto descriptivo de la fuente de atribución.
 */
export function getAttributionSource() {
    const urlParams = new URLSearchParams(window.location.search);
    const referrer = document.referrer ? document.referrer.toLowerCase() : '';
    const utmSource = urlParams.get('utm_source')?.toLowerCase();
    const utmMedium = urlParams.get('utm_medium')?.toLowerCase();
    const utmCampaign = urlParams.get('utm_campaign');
    const gclid = urlParams.get('gclid') || urlParams.get('gbraid') || urlParams.get('wbraid');

    const hasActiveCampaignParams = Boolean(gclid || utmSource || utmMedium || utmCampaign);

    // 1. Si no hay parámetros nuevos de campaña en la URL, intentar recuperar atribución previa
    if (!hasActiveCampaignParams) {
        try {
            const sessionCached = sessionStorage.getItem(SESSION_STORAGE_KEY);
            if (sessionCached) {
                return sessionCached;
            }
        } catch (_) {}

        const persistentRecord = getAttributionRecord();
        if (persistentRecord && persistentRecord.source) {
            try {
                sessionStorage.setItem(SESSION_STORAGE_KEY, persistentRecord.source);
            } catch (_) {}
            return persistentRecord.source;
        }
    }

    let source = '';

    // A. Google Ads (SEM / PPC)
    if (gclid || utmMedium === 'cpc' || utmMedium === 'ppc' || utmSource === 'google_ads' || utmSource === 'adwords') {
        source = '🎯 Google Ads (SEM)';
        if (utmCampaign) {
            source += ` — Campaña: ${utmCampaign}`;
        }
    }
    // B. Redes Sociales (Meta, LinkedIn, Instagram, X/Twitter, TikTok)
    else if (
        utmMedium === 'social' ||
        ['linkedin', 'facebook', 'instagram', 'twitter', 'x', 'tiktok'].includes(utmSource || '') ||
        referrer.includes('linkedin.com') ||
        referrer.includes('facebook.com') ||
        referrer.includes('instagram.com') ||
        referrer.includes('t.co') ||
        referrer.includes('x.com') ||
        referrer.includes('l.wl.co')
    ) {
        let platform = 'Social';
        if (utmSource?.includes('linkedin') || referrer.includes('linkedin') || referrer.includes('l.wl.co')) platform = 'LinkedIn';
        else if (utmSource?.includes('facebook') || referrer.includes('facebook')) platform = 'Facebook';
        else if (utmSource?.includes('instagram') || referrer.includes('instagram')) platform = 'Instagram';
        else if (utmSource?.includes('twitter') || utmSource?.includes('x') || referrer.includes('t.co') || referrer.includes('x.com')) platform = 'X (Twitter)';

        source = `📱 Redes Sociales (${platform})`;
        if (utmCampaign) {
            source += ` — Campaña: ${utmCampaign}`;
        }
    }
    // C. Búsqueda Orgánica (Google, Bing, DuckDuckGo, Yahoo)
    else if (referrer.includes('google.') || referrer.includes('bing.') || referrer.includes('duckduckgo.') || referrer.includes('yahoo.')) {
        let searchEngine = 'Google';
        if (referrer.includes('bing.')) searchEngine = 'Bing';
        else if (referrer.includes('duckduckgo.')) searchEngine = 'DuckDuckGo';
        else if (referrer.includes('yahoo.')) searchEngine = 'Yahoo';

        source = `🔍 Búsqueda Orgánica (${searchEngine})`;
    }
    // D. Enlace Referido Externo
    else if (referrer && !referrer.includes(window.location.hostname)) {
        try {
            const refHost = new URL(referrer).hostname.replace('www.', '');
            source = `🔗 Referido desde ${refHost}`;
        } catch (_) {
            source = '🔗 Referido externo';
        }
    }
    // E. Tráfico Directo
    else {
        source = '🌐 Tráfico Directo';
    }

    // Persistir en sessionStorage
    try {
        sessionStorage.setItem(SESSION_STORAGE_KEY, source);
    } catch (_) {}

    // Persistir en localStorage con ventana de 30 días para first-touch B2B
    try {
        /** @type {import('../types.js').AttributionRecord} */
        const record = {
            source,
            timestamp: Date.now(),
            landingPage: window.location.pathname,
            utmCampaign: utmCampaign || null,
            utmSource: utmSource || null,
            utmMedium: utmMedium || null,
            gclid: gclid || null,
        };
        localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(record));
    } catch (_) {}

    return source;
}
