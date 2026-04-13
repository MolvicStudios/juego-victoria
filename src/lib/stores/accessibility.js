import { writable } from 'svelte/store';
import { browser } from '$app/environment';

function loadBool(key, def = false) {
	if (!browser) return def;
	return localStorage.getItem(key) === '1';
}

/** Modo Flujo Silencioso — desactiva animaciones y partículas para menor estimulación sensorial */
export const quietMode = writable(loadBool('pp_quiet_mode'));

if (browser) {
	quietMode.subscribe(v => {
		localStorage.setItem('pp_quiet_mode', v ? '1' : '0');
		document.documentElement.classList.toggle('quiet-mode', v);
	});
}
