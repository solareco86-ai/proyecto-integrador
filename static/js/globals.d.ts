/**
 * Declaraciones globales ambientales (Ambient Declarations) para DataMaq.
 * Extiende la interfaz de Window para reconocer las variables inyectadas por los templates Jinja2.
 */

interface WindowAppConfig {
    apiUrl?: string;
    contactApiUrl?: string;
    gaId?: string;
    googleAdsId?: string;
    googleAdsConversionId?: string;
    googleAdsWhatsappConversionId?: string;
    clarityId?: string;
    telemetryApiUrl?: string;
    telemetryWsUrl?: string;
    debug?: boolean;
}

interface Window {
    APP_CONFIG?: WindowAppConfig;
    dataLayer?: any[];
    gtag?: (...args: any[]) => void;
    clarity?: (...args: any[]) => void;
}
