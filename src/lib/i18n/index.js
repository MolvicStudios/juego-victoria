/**
 * Motor i18n de PinguPlay — implementación manual con Svelte stores.
 * Sin dependencias externas. Carga síncrona (static imports → no flash).
 */
import { writable, derived } from 'svelte/store';
import { browser } from '$app/environment';

import es from './locales/es.json';
import en from './locales/en.json';
import ca from './locales/ca.json';
import eu from './locales/eu.json';
import gl from './locales/gl.json';

/** @type {Record<string, Record<string, string>>} */
const ALL = { es, en, ca, eu, gl };

/** Metadatos de cada idioma disponible */
export const LOCALES = /** @type {const} */ ({
	es: { name: 'Español',  nativeName: 'Español',  confirmBtn: '¡Vamos!'   },
	en: { name: 'English',  nativeName: 'English',  confirmBtn: "Let's go!" },
	ca: { name: 'Català',   nativeName: 'Català',   confirmBtn: 'Anem!'     },
	eu: { name: 'Euskera',  nativeName: 'Euskera',  confirmBtn: 'Goazen!'   },
	gl: { name: 'Galego',   nativeName: 'Galego',   confirmBtn: 'Imos!'     },
});

/** @returns {string} */
function detectLocale() {
	if (!browser) return 'es';
	try {
		const saved = localStorage.getItem('pp_locale');
		if (saved && saved in ALL) return saved;
		const nav = (navigator.language || '').slice(0, 2).toLowerCase();
		/** @type {Record<string,string>} */
		const MAP = { es: 'es', en: 'en', ca: 'ca', eu: 'eu', gl: 'gl' };
		return MAP[nav] || 'es';
	} catch { return 'es'; }
}

/** Store del locale activo */
export const locale = writable(detectLocale());

// Persistir en localStorage al cambiar
locale.subscribe(v => {
	if (browser) try { localStorage.setItem('pp_locale', v); } catch { /* noop */ }
});

/**
 * Store derivado: función de traducción reactiva.
 *
 * En plantillas: {$t('key')} o {$t('key', { name: 'Pingu' })}
 * En JS:         get(t)('key')
 */
export const t = derived(locale, ($locale) => {
	const dict     = ALL[$locale]   || ALL['es'];
	const fallback = ALL['es'];

	/**
	 * @param {string} key
	 * @param {Record<string, string|number>=} vars
	 * @returns {string}
	 */
	return (key, vars) => {
		let str = dict[key] ?? fallback[key] ?? key;
		if (vars) {
			for (const [k, v] of Object.entries(vars)) {
				str = str.replace(new RegExp(`\\{${k}\\}`, 'g'), String(v));
			}
		}
		return str;
	};
});

/**
 * Inicializa i18n — llamar en +layout.svelte onMount.
 * Con static imports la carga es instantánea.
 * @returns {Promise<void>}
 */
export async function initI18n() {
	locale.set(detectLocale());
}
