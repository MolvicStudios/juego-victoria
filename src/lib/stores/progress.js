import { writable, derived, get } from 'svelte/store';
import { browser } from '$app/environment';
import { activeProfileIndex } from './profiles.js';
import { MEDALS } from '../data.js';

const STORAGE_KEY = 'pp_progress';

function load() {
	if (!browser) return {};
	try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}'); } catch { return {}; }
}

/** @type {import('svelte/store').Writable<Record<string, any>>} */
const allProgress = writable(load());

if (browser) {
	allProgress.subscribe(v => localStorage.setItem(STORAGE_KEY, JSON.stringify(v)));
}

function profileKey() {
	const idx = get(activeProfileIndex);
	return idx >= 0 ? `p${idx}` : '__none';
}

function getProfileProgress() {
	const all = get(allProgress);
	const k = profileKey();
	return all[k] || { stars: 0, levels: {}, maxLevels: {}, correctStreak: {}, wrongStreak: {}, sessionGames: 0, sessionStars: 0, sessionCompleted: 0 };
}

/** @param {Record<string, any>} data */
function setProfileProgress(data) {
	allProgress.update(all => {
		all[profileKey()] = data;
		return { ...all };
	});
}

export { allProgress };

export function getStars() { return getProfileProgress().stars || 0; }
export function getLevels() { return getProfileProgress().levels || {}; }
export function getMaxLevels() { return getProfileProgress().maxLevels || {}; }

/** @param {number} gameNum */
export function getLevel(gameNum) {
	return (getProfileProgress().levels || {})[gameNum] || 1;
}

/**
 * @param {number} gameNum
 * @param {number} lv
 */
export function setLevel(gameNum, lv) {
	const d = getProfileProgress();
	if (!d.levels) d.levels = {};
	d.levels[gameNum] = lv;
	setProfileProgress(d);
}

/** @param {number} n */
export function addStars(n) {
	const d = getProfileProgress();
	d.stars = (d.stars || 0) + n;
	d.sessionStars = (d.sessionStars || 0) + n;
	setProfileProgress(d);
}

/**
 * Called on game complete. Advances level, updates maxLevels.
 * @param {number} gameNum
 * @returns {string} message about level change
 */
export function onGameComplete(gameNum) {
	const d = getProfileProgress();
	if (!d.levels) d.levels = {};
	if (!d.maxLevels) d.maxLevels = {};
	d.wrongStreak = d.wrongStreak || {};
	d.wrongStreak[gameNum] = 0;
	const lv = d.levels[gameNum] || 1;
	const nextLv = Math.min(lv + 1, 15);
	d.levels[gameNum] = nextLv;
	if (!d.maxLevels[gameNum] || nextLv > d.maxLevels[gameNum]) d.maxLevels[gameNum] = nextLv;
	d.correctStreak = d.correctStreak || {};
	d.correctStreak[gameNum] = 0;
	setProfileProgress(d);
	return lv < 15 ? '¡Nivel ' + nextLv + ' desbloqueado! 🚀' : '¡Eres un experto nivel 15! 🏆';
}

/** @param {number} gameNum */
export function onCorrect(gameNum) {
	const d = getProfileProgress();
	d.correctStreak = d.correctStreak || {};
	d.wrongStreak = d.wrongStreak || {};
	d.correctStreak[gameNum] = (d.correctStreak[gameNum] || 0) + 1;
	d.wrongStreak[gameNum] = 0;
	setProfileProgress(d);
}

/**
 * @param {number} gameNum
 * @returns {string|null} message if level dropped
 */
export function onWrong(gameNum) {
	const d = getProfileProgress();
	d.wrongStreak = d.wrongStreak || {};
	d.correctStreak = d.correctStreak || {};
	d.wrongStreak[gameNum] = (d.wrongStreak[gameNum] || 0) + 1;
	d.correctStreak[gameNum] = 0;
	const lv = (d.levels || {})[gameNum] || 1;
	if (d.wrongStreak[gameNum] >= 3 && lv > 1) {
		d.levels[gameNum] = lv - 1;
		d.wrongStreak[gameNum] = 0;
		setProfileProgress(d);
		return '¡Bajamos un poco! Nivel ' + (lv - 1);
	}
	setProfileProgress(d);
	return null;
}

export function resetSession() {
	const d = getProfileProgress();
	d.sessionGames = 0;
	d.sessionStars = 0;
	d.sessionCompleted = 0;
	setProfileProgress(d);
}

export function getStreak(/** @type {number} */ gameNum) {
	return (getProfileProgress().correctStreak || {})[gameNum] || 0;
}

export function getUnlockedMedals() {
	return getProfileProgress().medals || [];
}

/**
 * Checks all medals and returns any newly unlocked ones.
 * @param {number} gameNum
 * @returns {Array<{id:string, label:string, desc:string, icon:string}>}
 */
export function checkNewMedals(gameNum) {
	const d = getProfileProgress();
	const prev = d.medals || [];
	const streak = gameNum ? ((d.correctStreak || {})[gameNum] || 0) : 0;
	/** @type {Array<{id:string, label:string, desc:string, icon:string}>} */
	const newMedals = [];
	for (const medal of MEDALS) {
		if (prev.includes(medal.id)) continue;
		if (_medalCheck(medal.id, d, streak)) {
			prev.push(medal.id);
			newMedals.push(/** @type {{id:string, label:string, desc:string, icon:string}} */ (medal));
		}
	}
	if (newMedals.length > 0) { d.medals = prev; setProfileProgress(d); }
	return newMedals;
}

/** @param {string} id @param {any} d @param {number} streak @returns {boolean} */
function _medalCheck(id, d, streak) {
	switch (id) {
		case 'first_star':  return (d.stars || 0) >= 1;
		case 'streak3':     return streak >= 3;
		case 'streak5':     return streak >= 5;
		case 'stars50':     return (d.stars || 0) >= 50;
		case 'stars100':    return (d.stars || 0) >= 100;
		case 'stars500':    return (d.stars || 0) >= 500;
		case 'level5':      return Object.values(d.maxLevels || {}).some(v => v >= 5);
		case 'level10':     return Object.values(d.maxLevels || {}).some(v => v >= 10);
		case 'level15':     return Object.values(d.maxLevels || {}).some(v => v >= 15);
		case 'games5':      return (d.sessionCompleted || 0) >= 5;
		case 'games20':     return (d.sessionCompleted || 0) >= 20;
		case 'all_games':   return Object.keys(d.levels || {}).length >= 10;
		default:            return false;
	}
}

export function incrementSessionCompleted() {
	const d = getProfileProgress();
	d.sessionCompleted = (d.sessionCompleted || 0) + 1;
	setProfileProgress(d);
}

export function getSessionData() {
	const d = getProfileProgress();
	return { sessionGames: d.sessionGames || 0, sessionStars: d.sessionStars || 0, sessionCompleted: d.sessionCompleted || 0 };
}
