import { writable } from 'svelte/store';
import { browser } from '$app/environment';

/**
 * @typedef {{ name: string, avatar: string, pinguName: string, birthYear: number }} Profile
 */

const STORAGE_KEY = 'pp_profiles';
const ACTIVE_KEY = 'pp_activeProfile';

function loadProfiles() {
	if (!browser) return [];
	try {
		return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
	} catch { return []; }
}

function loadActiveIndex() {
	if (!browser) return -1;
	const v = parseInt(localStorage.getItem(ACTIVE_KEY) ?? '-1');
	return isNaN(v) ? -1 : v;
}

/** @type {import('svelte/store').Writable<Profile[]>} */
export const profiles = writable(loadProfiles());

/** @type {import('svelte/store').Writable<number>} */
export const activeProfileIndex = writable(loadActiveIndex());

if (browser) {
	profiles.subscribe(v => localStorage.setItem(STORAGE_KEY, JSON.stringify(v)));
	activeProfileIndex.subscribe(v => localStorage.setItem(ACTIVE_KEY, String(v)));
}

/**
 * Get the age range string for a given birth year.
 * @param {number} birthYear
 * @returns {'nubecitas'|'exploradores'|'aventureros'|'maestros'}
 */
export function ageRange(birthYear) {
	const age = new Date().getFullYear() - birthYear;
	if (age <= 2) return 'nubecitas';
	if (age <= 5) return 'exploradores';
	if (age <= 8) return 'aventureros';
	return 'maestros';
}

/** @param {Profile} p */
export function addProfile(p) {
	profiles.update(arr => {
		if (arr.length >= 4) return arr;
		return [...arr, p];
	});
}

/** @param {number} idx */
export function removeProfile(idx) {
	profiles.update(arr => arr.filter((_, i) => i !== idx));
	activeProfileIndex.update(v => v === idx ? -1 : v > idx ? v - 1 : v);
}

/** @param {number} idx */
export function setActiveProfile(idx) {
	activeProfileIndex.set(idx);
}
