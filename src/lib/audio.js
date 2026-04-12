import { get } from 'svelte/store';
import { muted } from './stores/settings.js';

let aCtx;

function au() {
	if (!aCtx) aCtx = new (window.AudioContext || window.webkitAudioContext)();
	return aCtx;
}

export function beep(freq = 440, dur = 0.3, type = 'sine', vol = 0.22) {
	if (get(muted)) return;
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

export function say(txt) {
	if (get(muted) || typeof window === 'undefined' || !window.speechSynthesis) return;
	speechSynthesis.cancel();
	const u = new SpeechSynthesisUtterance(txt);
	u.lang = 'es-ES'; u.rate = 0.85; u.pitch = 1.15;
	speechSynthesis.speak(u);
}

export function toggleMute() {
	muted.update(v => {
		const next = !v;
		if (next) speechSynthesis?.cancel();
		return next;
	});
}
