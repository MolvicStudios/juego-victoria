import { writable } from 'svelte/store';
import { browser } from '$app/environment';

function loadBool(key, def = false) {
	if (!browser) return def;
	return localStorage.getItem(key) === '1';
}

export const night = writable(loadBool('pp_night'));
export const muted = writable(loadBool('pp_muted'));
export const parentPin = writable(browser ? (localStorage.getItem('pp_parentPin') || '') : '');
export const hiContrast = writable(loadBool('pp_hc'));
export const bigText = writable(loadBool('pp_big'));

if (browser) {
	night.subscribe(v => localStorage.setItem('pp_night', v ? '1' : '0'));
	muted.subscribe(v => localStorage.setItem('pp_muted', v ? '1' : '0'));
	parentPin.subscribe(v => localStorage.setItem('pp_parentPin', v));
	hiContrast.subscribe(v => localStorage.setItem('pp_hc', v ? '1' : '0'));
	bigText.subscribe(v => localStorage.setItem('pp_big', v ? '1' : '0'));
}
