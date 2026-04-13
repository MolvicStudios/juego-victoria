<script>
	/**
	 * PinguCharacter — Pingüino SVG animable con 6 estados.
	 * Todos los estados se implementan como clases CSS sobre grupos SVG con IDs semánticos.
	 *
	 * ¿Por qué SVG con partes separadas?
	 * Permite animar alas, ojos, pico y cuerpo de forma independiente,
	 * creando un personaje expresivo que los niños reconocen como "vivo".
	 */

	/** @type {'idle'|'waiting'|'correct'|'wrong'|'excited'|'idle-long'} */
	let { state = 'idle', size = 120, worldTheme = 'nubecitas' } = $props();

	/** Colores del contorno/acento según el mundo */
	const WORLD_ACCENT = {
		nubecitas:    '#A78BFA',
		exploradores: '#4D9FEC',
		aventureros:  '#6BCB77',
		maestros:     '#FF9F43',
	};

	const accent = $derived(WORLD_ACCENT[worldTheme] || '#FF6B6B');

	/**
	 * Las estrellas decorativas para el estado "excited" se generan una vez.
	 * Posiciones relativas al SVG (viewBox 0 0 100 130).
	 */
	const STARS = [
		{ cx: 15, cy: 30, r: 4, delay: 0 },
		{ cx: 88, cy: 25, r: 3, delay: 220 },
		{ cx: 10, cy: 75, r: 3.5, delay: 440 },
	];
</script>

<svg
	class="pingu pingu-{state}"
	viewBox="0 0 100 130"
	width={size}
	height={size * 1.3}
	xmlns="http://www.w3.org/2000/svg"
	role="img"
	aria-label="Pingu"
>
	<!-- ── Pies / base ─────────────────────────────────────────────────── -->
	<g id="pingu-feet">
		<ellipse cx="37" cy="116" rx="12" ry="6" fill="#FF8C00"
			transform="rotate(-10 37 116)" />
		<ellipse cx="63" cy="116" rx="12" ry="6" fill="#FF8C00"
			transform="rotate(10 63 116)" />
	</g>

	<!-- ── Cuerpo principal ────────────────────────────────────────────── -->
	<g id="pingu-body" style="transform-origin:50px 75px">
		<!-- Cuerpo negro -->
		<ellipse cx="50" cy="75" rx="30" ry="38" fill="#1a1a2e" />
		<!-- Barriga blanca -->
		<ellipse cx="50" cy="82" rx="18" ry="24" fill="#f5f5f5" />
		<!-- Acento del mundo (borde sutil en barriga) -->
		<ellipse cx="50" cy="82" rx="18" ry="24" fill="none"
			stroke={accent} stroke-width="1.5" opacity="0.5" />
	</g>

	<!-- ── Ala izquierda ───────────────────────────────────────────────── -->
	<!-- transform-origin en la esquina superior derecha del ala -->
	<g id="pingu-wing-left" style="transform-origin:34px 62px">
		<ellipse cx="22" cy="78" rx="10" ry="22" fill="#1a1a2e"
			transform="rotate(-12 22 78)" />
		<!-- Detalle ala -->
		<ellipse cx="22" cy="78" rx="4" ry="10" fill="#2d2d4e"
			transform="rotate(-12 22 78)" />
	</g>

	<!-- ── Ala derecha ─────────────────────────────────────────────────── -->
	<!-- transform-origin en la esquina superior izquierda del ala -->
	<g id="pingu-wing-right" style="transform-origin:66px 62px">
		<ellipse cx="78" cy="78" rx="10" ry="22" fill="#1a1a2e"
			transform="rotate(12 78 78)" />
		<ellipse cx="78" cy="78" rx="4" ry="10" fill="#2d2d4e"
			transform="rotate(12 78 78)" />
	</g>

	<!-- ── Pico ────────────────────────────────────────────────────────── -->
	<!-- transform-origin en el centro superior del pico -->
	<g id="pingu-beak" style="transform-origin:50px 50px">
		<ellipse cx="50" cy="55" rx="8" ry="5.5" fill="#FF8C00" />
		<!-- Hendidura del pico -->
		<line x1="43" y1="55" x2="57" y2="55" stroke="#cc6600" stroke-width="1.2" />
	</g>

	<!-- ── Ojo izquierdo ──────────────────────────────────────────────── -->
	<g id="pingu-eye-left" style="transform-origin:40px 45px">
		<circle cx="40" cy="45" r="8" fill="white" />
		<circle cx="41.5" cy="46" r="5" fill="#1a1a2e" />
		<!-- Pupila reflejo -->
		<circle cx="43" cy="44" r="1.8" fill="white" />
	</g>

	<!-- ── Ojo derecho ────────────────────────────────────────────────── -->
	<g id="pingu-eye-right" style="transform-origin:60px 45px">
		<circle cx="60" cy="45" r="8" fill="white" />
		<circle cx="61.5" cy="46" r="5" fill="#1a1a2e" />
		<circle cx="63" cy="44" r="1.8" fill="white" />
	</g>

	<!-- ── Estrellas "excited" (ocultas por defecto) ──────────────────── -->
	{#each STARS as s}
		<g class="pingu-excited-star" style="transform-origin:{s.cx}px {s.cy}px;animation-delay:{s.delay}ms">
			<!-- Estrella SVG de 4 puntas simplificada -->
			<polygon
				points="{s.cx},{s.cy - s.r} {s.cx + s.r * 0.4},{s.cy - s.r * 0.4} {s.cx + s.r},{s.cy} {s.cx + s.r * 0.4},{s.cy + s.r * 0.4} {s.cx},{s.cy + s.r} {s.cx - s.r * 0.4},{s.cy + s.r * 0.4} {s.cx - s.r},{s.cy} {s.cx - s.r * 0.4},{s.cy - s.r * 0.4}"
				fill="#FFD700"
			/>
		</g>
	{/each}
</svg>

<style>
	/* ── Base ─────────────────────────────────────────────────────────── */
	.pingu {
		display: block;
		overflow: visible; /* las alas asoman un poco fuera del viewBox */
		flex-shrink: 0;
	}

	/* ── Estado idle — siempre activo ─────────────────────────────────── */
	/* Respiración suave del cuerpo */
	.pingu :global(#pingu-body) {
		animation: pingu-breathe 2.2s ease-in-out infinite;
	}

	/* Parpadeo natural cada ~3s */
	.pingu :global(#pingu-eye-left),
	.pingu :global(#pingu-eye-right) {
		animation: pingu-blink 3s ease-in-out infinite;
	}
	/* Offset para que los dos ojos no parpadeén exactamente igual */
	.pingu :global(#pingu-eye-right) {
		animation-delay: 0.08s;
	}

	/* Las estrellas excited están ocultas por defecto */
	.pingu :global(.pingu-excited-star) {
		opacity: 0;
		pointer-events: none;
	}

	/* ── Estado correct ───────────────────────────────────────────────── */
	.pingu-correct :global(#pingu-wing-left) {
		animation: pingu-wing-flap-l 0.6s ease-out;
	}
	.pingu-correct :global(#pingu-wing-right) {
		animation: pingu-wing-flap-r 0.6s ease-out;
	}
	.pingu-correct :global(#pingu-body) {
		animation: pingu-jump 0.6s ease-out, pingu-breathe 2.2s ease-in-out 0.7s infinite;
	}
	.pingu-correct :global(#pingu-eye-left),
	.pingu-correct :global(#pingu-eye-right) {
		animation: pingu-eyes-wide 0.4s ease-out;
	}

	/* ── Estado wrong ─────────────────────────────────────────────────── */
	.pingu-wrong :global(#pingu-body) {
		animation: pingu-head-shake 0.5s ease-in-out, pingu-breathe 2.2s ease-in-out 0.6s infinite;
	}
	.pingu-wrong :global(#pingu-eye-left),
	.pingu-wrong :global(#pingu-eye-right) {
		animation: pingu-frown 0.5s ease-in-out;
	}
	.pingu-wrong :global(#pingu-wing-left),
	.pingu-wrong :global(#pingu-wing-right) {
		animation: pingu-wings-droop 0.5s ease-in-out;
	}

	/* ── Estado waiting ───────────────────────────────────────────────── */
	.pingu-waiting :global(#pingu-body) {
		animation: pingu-head-tilt 2s ease-in-out 3,
		pingu-breathe 2.2s ease-in-out infinite;
	}

	/* ── Estado excited ───────────────────────────────────────────────── */
	/* Animaciones intensificadas x1.5 */
	.pingu-excited :global(#pingu-wing-left) {
		animation: pingu-wing-flap-l 0.4s ease-out infinite alternate;
	}
	.pingu-excited :global(#pingu-wing-right) {
		animation: pingu-wing-flap-r 0.4s ease-out infinite alternate;
	}
	.pingu-excited :global(#pingu-body) {
		animation: pingu-jump 0.4s ease-out infinite, pingu-breathe 2.2s ease-in-out infinite;
	}
	/* Estrellas visibles en excited */
	.pingu-excited :global(.pingu-excited-star) {
		animation: pingu-star-pulse 0.6s ease-in-out infinite alternate;
	}

	/* ── Estado idle-long (bostezo) ───────────────────────────────────── */
	.pingu-idle-long :global(#pingu-beak) {
		animation: pingu-yawn 1s ease-in-out;
	}
	.pingu-idle-long :global(#pingu-wing-right) {
		animation: pingu-point 0.5s ease-out 1.1s both;
	}

	/* ── Keyframes ────────────────────────────────────────────────────── */
	@keyframes pingu-breathe {
		0%, 100% { transform: scaleY(1); }
		50%       { transform: scaleY(1.015); }
	}

	/* El parpadeo comprime scaleY el ojo entero */
	@keyframes pingu-blink {
		0%, 90%, 100%  { transform: scaleY(1); }
		95%             { transform: scaleY(0.1); }
	}

	/* Aletas suben 40° */
	@keyframes pingu-wing-flap-l {
		0%   { transform: rotate(0deg); }
		35%  { transform: rotate(-40deg); }
		100% { transform: rotate(0deg); }
	}
	@keyframes pingu-wing-flap-r {
		0%   { transform: rotate(0deg); }
		35%  { transform: rotate(40deg); }
		100% { transform: rotate(0deg); }
	}

	/* Pequeño salto vertical */
	@keyframes pingu-jump {
		0%   { transform: translateY(0) scaleY(1); }
		30%  { transform: translateY(-8px) scaleY(1.02); }
		100% { transform: translateY(0) scaleY(1); }
	}

	/* Ojos abiertos de emoción: scaleX más ancho */
	@keyframes pingu-eyes-wide {
		0%   { transform: scaleX(1); }
		25%  { transform: scaleX(1.3); }
		100% { transform: scaleX(1); }
	}

	/* Negar con la cabeza */
	@keyframes pingu-head-shake {
		0%   { transform: rotate(0deg); }
		20%  { transform: rotate(-5deg); }
		60%  { transform: rotate(5deg); }
		100% { transform: rotate(0deg); }
	}

	/* Ceño fruncido: ojos comprimidos en Y */
	@keyframes pingu-frown {
		0%   { transform: scaleY(1); }
		40%  { transform: scaleY(0.7); }
		100% { transform: scaleY(1); }
	}

	/* Alas caídas ligeramente */
	@keyframes pingu-wings-droop {
		0%   { transform: rotate(0deg); }
		50%  { transform: rotate(10deg); }
		100% { transform: rotate(0deg); }
	}

	/* Inclinar la cabeza (estado waiting) */
	@keyframes pingu-head-tilt {
		0%, 100%  { transform: rotate(0deg); }
		30%, 70%  { transform: rotate(-10deg); }
	}

	/* Bostezo — pico se abre (scaleY) */
	@keyframes pingu-yawn {
		0%   { transform: scaleY(1); }
		40%  { transform: scaleY(1.6); }
		80%  { transform: scaleY(1.6); }
		100% { transform: scaleY(1); }
	}

	/* Señalar con el ala derecha */
	@keyframes pingu-point {
		0%   { transform: rotate(0deg); }
		100% { transform: rotate(-30deg); }
	}

	/* Estrellas excited pulsantes */
	@keyframes pingu-star-pulse {
		0%   { opacity: 0; transform: scale(0.5); }
		100% { opacity: 1; transform: scale(1.2); }
	}

	/* ── Respeta prefers-reduced-motion ──────────────────────────────── */
	@media (prefers-reduced-motion: reduce) {
		.pingu :global(*) {
			animation: none !important;
			transition: none !important;
		}
	}
</style>
