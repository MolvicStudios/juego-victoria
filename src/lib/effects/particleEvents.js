/**
 * particleEvents — cola de eventos de partículas para ParticleEngine.
 * ParticleEngine.svelte suscribe a este store y renderiza los grupos.
 * GameShell (u otros) llaman a trigger() para emitir efectos.
 */
import { writable } from 'svelte/store';

/** @typedef {{ id: number, items: Array<any> }} ParticleGroup */

/** @type {import('svelte/store').Writable<ParticleGroup[]>} */
export const particleGroups = writable([]);

let uid = 0;

/** Color primario de partículas por mundo */
const WORLD_PRIMARY = {
	nubecitas:    '#A78BFA',
	exploradores: '#4D9FEC',
	aventureros:  '#6BCB77',
	maestros:     '#FF9F43',
};

/**
 * Dispara un efecto de partículas.
 * Seguro de llamar aunque ParticleEngine no esté montado (no hace nada).
 * @param {'correct'|'wrong'|'levelComplete'|'confetti'} type
 * @param {number} x
 * @param {number} y
 * @param {string} [worldTheme]
 */
export function trigger(type, x, y, worldTheme = 'nubecitas') {
	if (typeof window === 'undefined') return;

	const primary = WORLD_PRIMARY[worldTheme] || '#A78BFA';
	const gid = ++uid;
	/** @type {Array<any>} */
	let items = [];

	if (type === 'correct') {
		for (let i = 0; i < 10; i++) {
			const angle = -160 + i * 32;
			const rad = (angle * Math.PI) / 180;
			const dist = 55 + Math.random() * 40;
			items.push({
				id: uid * 1000 + i,
				x, y,
				dx: Math.sin(rad) * dist,
				dy: -Math.abs(Math.cos(rad)) * dist,
				color: i % 2 === 0 ? '#FFD700' : primary,
				size: 8 + Math.floor(Math.random() * 5),
				dur: 560 + Math.random() * 80,
				type: 'star',
				delay: 0,
				gravity: false,
				rotate: Math.random() * 360,
			});
		}
		setTimeout(() => removeGroup(gid), 700);

	} else if (type === 'wrong') {
		for (let i = 0; i < 5; i++) {
			const side = i % 2 === 0 ? 1 : -1;
			items.push({
				id: uid * 1000 + i,
				x, y,
				dx: side * (20 + Math.random() * 40),
				dy: -10 + Math.random() * 20,
				color: '#FF4444',
				size: 6,
				dur: 380,
				type: 'circle',
				delay: i * 25,
				gravity: true,
				rotate: 0,
			});
		}
		setTimeout(() => removeGroup(gid), 500);

	} else {
		// levelComplete / confetti
		const confColors = [primary, '#FFD700', '#FF6B6B', '#6BCB77', '#4D9FEC', '#F472B6', '#fff'];
		const shapes = /** @type {const} */(['rect', 'circle', 'star']);
		const vw = window.innerWidth || 400;
		for (let i = 0; i < 120; i++) {
			items.push({
				id: uid * 1000 + i,
				x: Math.random() * vw,
				y: -10,
				dx: (Math.random() - 0.5) * 80,
				dy: 80 + Math.random() * 120,
				color: confColors[Math.floor(Math.random() * confColors.length)],
				size: 6 + Math.floor(Math.random() * 7),
				dur: 1800 + Math.random() * 700,
				type: shapes[Math.floor(Math.random() * shapes.length)],
				delay: Math.random() * 800,
				gravity: true,
				rotate: Math.random() * 360,
			});
		}
		setTimeout(() => removeGroup(gid), 3000);
	}

	if (items.length) {
		particleGroups.update(gs => [...gs, { id: gid, items }]);
	}
}

/** @param {number} gid */
function removeGroup(gid) {
	particleGroups.update(gs => gs.filter(g => g.id !== gid));
}
