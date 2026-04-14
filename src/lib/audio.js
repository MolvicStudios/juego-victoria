import { get } from 'svelte/store';
import { browser } from '$app/environment';
import { muted } from './stores/settings.js';
import { locale } from '$lib/i18n/index.js';

/** @type {AudioContext|undefined} */
let aCtx;
let _userInteracted = false;

if (browser) {
	const _onInteract = () => { _userInteracted = true; };
	document.addEventListener('click',      _onInteract, { once: true, passive: true, capture: true });
	document.addEventListener('touchstart', _onInteract, { once: true, passive: true, capture: true });
	document.addEventListener('keydown',    _onInteract, { once: true, passive: true, capture: true });
}

function au() {
	if (!aCtx) aCtx = new (window.AudioContext || window.webkitAudioContext)();
	return aCtx;
}

function notifySoundUI() {
	try { if (typeof document !== 'undefined') document.dispatchEvent(new CustomEvent('pp-sound')); } catch {}
}

/** @param {number} [freq] @param {number} [dur] @param {OscillatorType} [type] @param {number} [vol] */
export function beep(freq = 440, dur = 0.3, type = 'sine', vol = 0.22) {
	if (get(muted)) return;
	notifySoundUI();
	try {
		const c = au(), o = c.createOscillator(), g = c.createGain();
		o.connect(g); g.connect(c.destination); o.type = type; o.frequency.value = freq;
		g.gain.setValueAtTime(vol, c.currentTime);
		g.gain.exponentialRampToValueAtTime(0.001, c.currentTime + dur);
		o.start(); o.stop(c.currentTime + dur);
	} catch {}
}

export function winSound() {
	[523, 659, 784, 1047].forEach((f, i) => setTimeout(() => beep(f, 0.22, 'sine', 0.28), i * 100));
}

export function boo() { beep(150, 0.28, 'sawtooth', 0.16); }

export function fanfare() {
	[523, 523, 659, 784, 659, 784, 1047].forEach((f, i) => setTimeout(() => beep(f, 0.18, 'sine', 0.25), i * 90));
}

// Mapa locale PinguPlay → código BCP-47 para Web Speech API
/** @type {Record<string,string>} */
const SPEECH_LANG = {
	es: 'es-ES',
	en: 'en-US',
	ca: 'ca-ES',
	eu: 'eu-ES',
	gl: 'gl-ES',
};

/** @param {string} txt */
export function say(txt) {
	if (!_userInteracted || get(muted) || typeof window === 'undefined' || !window.speechSynthesis) return;
	notifySoundUI();
	speechSynthesis.cancel();
	const u = new SpeechSynthesisUtterance(txt);
	u.lang = SPEECH_LANG[get(locale)] ?? 'es-ES';
	u.rate = 0.85;
	u.pitch = 1.15;
	speechSynthesis.speak(u);
}

export function toggleMute() {
	muted.update(v => {
		const next = !v;
		if (next) speechSynthesis?.cancel();
		return next;
	});
}

// ── Sonidos temáticos v3 ────────────────────────────────────────────────────

/**
 * Acorde mayor alegre para respuesta correcta (Do-Mi-Sol).
 * Tres osciladores en secuencia rápida con envelope suave.
 */
export function playCorrect() {
	if (get(muted)) return;
	notifySoundUI();
	try {
		const c = au();
		[523, 659, 784].forEach((freq, i) => {
			setTimeout(() => {
				const o = c.createOscillator(), g = c.createGain();
				o.connect(g); g.connect(c.destination);
				o.type = 'sine'; o.frequency.value = freq;
				const t = c.currentTime;
				g.gain.setValueAtTime(0, t);
				g.gain.linearRampToValueAtTime(0.22, t + 0.01);
				g.gain.setValueAtTime(0.22 * 0.7, t + 0.06);
				g.gain.linearRampToValueAtTime(0, t + 0.28);
				o.start(t); o.stop(t + 0.3);
			}, i * 80);
		});
	} catch {}
}

/**
 * Error suave para respuesta incorrecta.
 * Tono descendente con vibrato leve — no agresivo para niños.
 */
export function playWrong() {
	if (get(muted)) return;
	notifySoundUI();
	try {
		const c = au();
		const o = c.createOscillator(), g = c.createGain();
		// LFO para vibrato suave
		const lfo = c.createOscillator(), lfoGain = c.createGain();
		lfo.frequency.value = 8; lfoGain.gain.value = 8;
		lfo.connect(lfoGain); lfoGain.connect(o.frequency);
		o.connect(g); g.connect(c.destination);
		o.type = 'sawtooth';
		o.frequency.setValueAtTime(220, c.currentTime);
		o.frequency.linearRampToValueAtTime(185, c.currentTime + 0.22);
		g.gain.setValueAtTime(0.14, c.currentTime);
		g.gain.linearRampToValueAtTime(0, c.currentTime + 0.25);
		lfo.start(); o.start();
		lfo.stop(c.currentTime + 0.26); o.stop(c.currentTime + 0.26);
	} catch {}
}

/**
 * Fanfarria de 4 notas para nivel completado.
 * Oscilador triangle con sensación de logro.
 */
export function playLevelComplete() {
	if (get(muted)) return;
	notifySoundUI();
	try {
		const c = au();
		[523, 659, 784, 1047].forEach((freq, i) => {
			setTimeout(() => {
				const o = c.createOscillator(), g = c.createGain();
				o.connect(g); g.connect(c.destination);
				o.type = 'triangle'; o.frequency.value = freq;
				const t = c.currentTime;
				g.gain.setValueAtTime(0.25, t);
				g.gain.linearRampToValueAtTime(0, t + 0.18);
				o.start(t); o.stop(t + 0.2);
			}, i * 150);
		});
	} catch {}
}

/**
 * Click sutil para feedback de temporizador.
 */
export function playTick() {
	if (get(muted)) return;
	try {
		const c = au(), o = c.createOscillator(), g = c.createGain();
		o.connect(g); g.connect(c.destination);
		o.type = 'sine'; o.frequency.value = 800;
		g.gain.setValueAtTime(0.12, c.currentTime);
		g.gain.linearRampToValueAtTime(0, c.currentTime + 0.03);
		o.start(); o.stop(c.currentTime + 0.035);
	} catch {}
}
