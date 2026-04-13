<script>
	/**
	 * WorldTransition — Envuelve el contenido de un juego/pantalla con una
	 * transición de entrada temática por mundo (600ms, GPU-acelerada con clip-path).
	 *
	 * Uso: <WorldTransition world="nubecitas">...contenido...</WorldTransition>
	 *
	 * Degradación progresiva:
	 * - Si clip-path no está soportado → fade simple.
	 * - Si prefers-reduced-motion → fade de 200ms.
	 */
	import { onMount } from 'svelte';

	/** @type {string} */
	let { world = 'nubecitas', children } = $props();

	let ready = $state(false);
	let supportsClipPath = $state(true);
	let reducedMotion = $state(false);

	onMount(() => {
		reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
		// Detectar soporte de clip-path (CSS.supports no cubre clip-path polygon en todos los navegadores,
		// así que usamos una prueba funcional)
		try {
			const el = document.createElement('div');
			el.style.clipPath = 'polygon(0 0, 100% 0, 100% 100%, 0 100%)';
			supportsClipPath = el.style.clipPath !== '';
		} catch {
			supportsClipPath = false;
		}
		// Forzar un reflow antes de añadir la clase "ready" para disparar la transición CSS
		requestAnimationFrame(() => {
			requestAnimationFrame(() => { ready = true; });
		});
	});
</script>

<!--
  La clase dinámica combina el mundo y el estado "ready".
  El CSS de abajo define las keyframes de entrada para cada mundo.
-->
<div
	class="wt wt-{world} {ready ? 'wt-in' : 'wt-start'} {reducedMotion ? 'wt-reduced' : ''} {!supportsClipPath ? 'wt-fallback' : ''}"
	aria-live="polite"
>
	{@render children?.()}
</div>

<style>
	/* ── Base ─────────────────────────────────────────────────── */
	.wt {
		position: relative;
		width: 100%;
		height: 100%;
		flex: 1;
		display: flex;
		flex-direction: column;
	}

	/* Estado inicial: invisible */
	.wt-start { opacity: 0; }

	/* ── Fallback (sin clip-path o reduced-motion): fade ──── */
	.wt-fallback.wt-start,
	.wt-reduced.wt-start { opacity: 0; }

	.wt-fallback.wt-in,
	.wt-reduced.wt-in {
		opacity: 1;
		transition: opacity 200ms ease-out;
	}

	/* ── Nubecitas: elipse desde arriba ────────────────────── */
	.wt-nubecitas.wt-start:not(.wt-fallback):not(.wt-reduced) {
		clip-path: ellipse(150% 60% at 50% -10%);
		opacity: 0;
		transform: translateY(-8px);
	}
	.wt-nubecitas.wt-in:not(.wt-fallback):not(.wt-reduced) {
		clip-path: ellipse(150% 150% at 50% 50%);
		opacity: 1;
		transform: translateY(0);
		transition:
			clip-path 600ms cubic-bezier(0.22, 1, 0.36, 1),
			opacity 400ms ease-out,
			transform 600ms cubic-bezier(0.22, 1, 0.36, 1);
	}

	/* ── Exploradores: zoom-out desde el centro ────────────── */
	.wt-exploradores.wt-start:not(.wt-fallback):not(.wt-reduced) {
		opacity: 0;
		transform: scale(0.3);
		transform-origin: center center;
	}
	.wt-exploradores.wt-in:not(.wt-fallback):not(.wt-reduced) {
		opacity: 1;
		transform: scale(1);
		transform-origin: center center;
		transition:
			opacity 400ms ease-out,
			transform 600ms cubic-bezier(0.22, 1, 0.36, 1);
	}

	/* ── Aventureros: puerta que se abre (clip-path lateral) ─ */
	.wt-aventureros.wt-start:not(.wt-fallback):not(.wt-reduced) {
		clip-path: polygon(45% 0%, 55% 0%, 55% 100%, 45% 100%);
		opacity: 0;
	}
	.wt-aventureros.wt-in:not(.wt-fallback):not(.wt-reduced) {
		clip-path: polygon(0% 0%, 100% 0%, 100% 100%, 0% 100%);
		opacity: 1;
		transition:
			clip-path 600ms cubic-bezier(0.22, 1, 0.36, 1),
			opacity 300ms ease-out;
	}

	/* ── Maestros: cortina desde arriba ────────────────────── */
	.wt-maestros.wt-start:not(.wt-fallback):not(.wt-reduced) {
		opacity: 0;
		transform: translateY(-100%);
	}
	.wt-maestros.wt-in:not(.wt-fallback):not(.wt-reduced) {
		opacity: 1;
		transform: translateY(0);
		transition:
			opacity 400ms ease-out,
			transform 600ms cubic-bezier(0.22, 1, 0.36, 1);
	}
</style>
