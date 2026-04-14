<script>
	/**
	 * WorldBackground — Fondos parallax SVG inline por mundo.
	 * Cero imágenes rasterizadas. Todo generado con SVG + CSS.
	 * Máximo ~8KB por fondo.
	 *
	 * Performance:
	 * - IntersectionObserver pausa animaciones fuera del viewport.
	 * - Dispositivos de baja gama (hardwareConcurrency < 4): solo gradiente.
	 * - prefers-reduced-motion: fondos estáticos.
	 */
	import { onMount, onDestroy } from 'svelte';
	import { quietMode } from '$lib/stores/accessibility.js';

	/** @type {{ world?: string, interactive?: boolean }} */
	let { world = 'nubecitas', interactive = true } = $props();

	let paused = $state(false);
	let lowPerf = $state(false);
	let reducedMotion = $state(false);
	let isQuiet = $state(false);
	quietMode.subscribe(v => { isQuiet = v; });

	// Offsets de parallax para cada capa (responden a mousemove / deviceOrientation)
	let p1x = $state(0), p2x = $state(0), p3x = $state(0), p4x = $state(0);

	/** @type {HTMLDivElement|null} */
	let bgEl = $state(null);
	/** @type {IntersectionObserver|null} */
	let observer = null;

	const LAYERS = [0.1, 0.3, 0.6, 1.0]; // factores de parallax por capa

	function onMouseMove(/** @type {MouseEvent} */ e) {
		if (!interactive || paused || reducedMotion || isQuiet || lowPerf) return;
		const cx = (e.clientX / window.innerWidth - 0.5) * 20;
		p1x = cx * LAYERS[0];
		p2x = cx * LAYERS[1];
		p3x = cx * LAYERS[2];
		p4x = cx * LAYERS[3];
	}

	function onOrientation(/** @type {DeviceOrientationEvent} */ e) {
		if (!interactive || paused || reducedMotion || isQuiet || lowPerf) return;
		const gamma = Math.max(-15, Math.min(15, e.gamma || 0)) / 15;
		p1x = gamma * LAYERS[0] * 15;
		p2x = gamma * LAYERS[1] * 15;
		p3x = gamma * LAYERS[2] * 15;
		p4x = gamma * LAYERS[3] * 15;
	}

	onMount(() => {
		reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
		lowPerf = (navigator.hardwareConcurrency || 4) < 4;

		if (bgEl) {
			observer = new IntersectionObserver(entries => {
				paused = !entries[0].isIntersecting;
			}, { threshold: 0 });
			observer.observe(bgEl);
		}

		if (interactive && !reducedMotion && !lowPerf) {
			window.addEventListener('mousemove', onMouseMove, { passive: true });
			if (typeof DeviceOrientationEvent !== 'undefined') {
				window.addEventListener('deviceorientation', onOrientation, { passive: true });
			}
		}
	});

	onDestroy(() => {
		observer?.disconnect();
		window.removeEventListener('mousemove', onMouseMove);
		if (typeof DeviceOrientationEvent !== 'undefined') {
			window.removeEventListener('deviceorientation', onOrientation);
		}
	});
</script>

<div class="world-bg world-bg-{world} {paused || reducedMotion || isQuiet ? 'world-bg-static' : ''}" bind:this={bgEl} aria-hidden="true">

	<!-- ──────────────── NUBECITAS ──────────────── -->
	{#if world === 'nubecitas'}
		<!-- Capa 1: cielo azul pálido (fondo estático) -->
		<div class="wb-layer wb-l1" style="transform:translateX({p1x}px)">
			<svg viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice">
				<defs>
					<linearGradient id="sky-n" x1="0" y1="0" x2="0" y2="1">
						<stop offset="0%" stop-color="#B8D9F5"/>
						<stop offset="100%" stop-color="#E8F4FF"/>
					</linearGradient>
				</defs>
				<rect width="400" height="200" fill="url(#sky-n)"/>
			</svg>
		</div>
		<!-- Capa 2: nubes grandes lentas -->
		<div class="wb-layer wb-l2 cloud-slow" style="transform:translateX({p2x}px)">
			<svg viewBox="0 0 800 200" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice">
				<!-- Nube 1 -->
				<ellipse cx="120" cy="80" rx="70" ry="35" fill="white" opacity="0.82"/>
				<ellipse cx="90"  cy="90" rx="45" ry="28" fill="white" opacity="0.82"/>
				<ellipse cx="160" cy="88" rx="42" ry="25" fill="white" opacity="0.82"/>
				<!-- Nube 2 -->
				<ellipse cx="420" cy="55" rx="60" ry="30" fill="white" opacity="0.75"/>
				<ellipse cx="390" cy="64" rx="38" ry="22" fill="white" opacity="0.75"/>
				<ellipse cx="460" cy="62" rx="36" ry="20" fill="white" opacity="0.75"/>
				<!-- Nube 3 -->
				<ellipse cx="700" cy="95" rx="55" ry="28" fill="white" opacity="0.78"/>
				<ellipse cx="668" cy="104" rx="35" ry="20" fill="white" opacity="0.78"/>
			</svg>
		</div>
		<!-- Capa 3: nubes medianas más rápidas -->
		<div class="wb-layer wb-l3 cloud-fast" style="transform:translateX({p3x}px)">
			<svg viewBox="0 0 600 200" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice">
				<ellipse cx="80"  cy="120" rx="38" ry="18" fill="#EAF3FF" opacity="0.9"/>
				<ellipse cx="55"  cy="128" rx="24" ry="14" fill="#EAF3FF" opacity="0.9"/>
				<ellipse cx="350" cy="100" rx="44" ry="20" fill="#EAF3FF" opacity="0.85"/>
				<ellipse cx="318" cy="108" rx="28" ry="15" fill="#EAF3FF" opacity="0.85"/>
				<ellipse cx="540" cy="140" rx="32" ry="15" fill="#EAF3FF" opacity="0.8"/>
			</svg>
		</div>
		<!-- Capa 4: copos de nieve / estrellitas parpadeantes -->
		<div class="wb-layer wb-l4" style="transform:translateX({p4x}px)">
			<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
				{#each [{x:40,y:60,d:0},{x:120,y:130,d:0.5},{x:200,y:50,d:1},{x:280,y:140,d:1.5},{x:360,y:80,d:0.2},{x:80,y:220,d:2},{x:320,y:250,d:0.8}] as s}
					<circle cx={s.x} cy={s.y} r="3" fill="#A78BFA" opacity="0.6"
						style="animation:snow-fall 4s linear {s.d}s infinite"/>
				{/each}
			</svg>
		</div>

	<!-- ──────────────── EXPLORADORES ──────────────── -->
	{:else if world === 'exploradores'}
		<div class="wb-layer wb-l1" style="transform:translateX({p1x}px)">
			<svg viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice">
				<defs>
					<linearGradient id="sky-e" x1="0" y1="0" x2="0" y2="1">
						<stop offset="0%" stop-color="#87CEEB"/>
						<stop offset="100%" stop-color="#C8E6F5"/>
					</linearGradient>
				</defs>
				<rect width="400" height="200" fill="url(#sky-e)"/>
			</svg>
		</div>
		<!-- Montañas lejanas (azul grisáceo) -->
		<div class="wb-layer wb-l2" style="transform:translateX({p2x}px)">
			<svg viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice">
				<path d="M0,140 L60,80 L120,110 L180,70 L240,100 L300,65 L360,95 L400,75 L400,200 L0,200Z" fill="#B0BEC5" opacity="0.65"/>
			</svg>
		</div>
		<!-- Colinas verdes medias -->
		<div class="wb-layer wb-l3" style="transform:translateX({p3x}px)">
			<svg viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice">
				<path d="M0,160 Q80,110 160,140 Q240,108 320,138 Q370,120 400,135 L400,200 L0,200Z" fill="#558B2F" opacity="0.8"/>
			</svg>
		</div>
		<!-- Árboles primer plano + pájaros -->
		<div class="wb-layer wb-l4" style="transform:translateX({p4x}px)">
			<svg viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice">
				<!-- Árboles triangulares -->
				{#each [{x:20,h:60},{x:60,h:50},{x:340,h:65},{x:380,h:48}] as t}
					<polygon points="{t.x},{200-t.h} {t.x-18},{200} {t.x+18},{200}" fill="#2E7D32" opacity="0.95"/>
					<polygon points="{t.x},{200-t.h-20} {t.x-13},{200-t.h+10} {t.x+13},{200-t.h+10}" fill="#388E3C" opacity="0.9"/>
				{/each}
				<!-- Pájaros volando (path en V) -->
				<path class="bird bird1" d="M100,60 Q108,54 116,60 Q124,54 132,60" fill="none" stroke="#555" stroke-width="2" stroke-linecap="round"/>
				<path class="bird bird2" d="M250,45 Q258,39 266,45 Q274,39 282,45" fill="none" stroke="#555" stroke-width="1.5" stroke-linecap="round"/>
			</svg>
		</div>

	<!-- ──────────────── AVENTUREROS ──────────────── -->
	{:else if world === 'aventureros'}
		<div class="wb-layer wb-l1" style="transform:translateX({p1x}px)">
			<svg viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice">
				<defs>
					<linearGradient id="sea-a" x1="0" y1="0" x2="0" y2="1">
						<stop offset="0%" stop-color="#0D47A1" opacity="0.9"/>
						<stop offset="60%" stop-color="#0288D1"/>
						<stop offset="100%" stop-color="#26C6DA"/>
					</linearGradient>
				</defs>
				<rect width="400" height="200" fill="url(#sea-a)"/>
				<!-- Sol -->
				<circle cx="340" cy="40" r="28" fill="#FFD600" opacity="0.9"/>
				<circle cx="340" cy="40" r="36" fill="#FFF176" opacity="0.3"/>
			</svg>
		</div>
		<!-- Olas medias -->
		<div class="wb-layer wb-l2 wave-slow" style="transform:translateX({p2x}px)">
			<svg viewBox="0 0 800 200" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice">
				<path d="M0,130 Q100,110 200,130 Q300,150 400,130 Q500,110 600,130 Q700,150 800,130 L800,200 L0,200Z"
					fill="#0097A7" opacity="0.55"/>
			</svg>
		</div>
		<!-- Olas primer plano más rápidas -->
		<div class="wb-layer wb-l3 wave-fast" style="transform:translateX({p3x}px)">
			<svg viewBox="0 0 800 200" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice">
				<path d="M0,155 Q80,140 160,155 Q240,170 320,155 Q400,140 480,155 Q560,170 640,155 Q720,140 800,155 L800,200 L0,200Z"
					fill="#00BCD4" opacity="0.65"/>
			</svg>
		</div>
		<!-- Burbujas -->
		<div class="wb-layer wb-l4" style="transform:translateX({p4x}px)">
			<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
				{#each [{cx:50,cy:280,r:6,d:0},{cx:130,cy:260,r:4,d:1},{cx:220,cy:290,r:7,d:0.5},{cx:310,cy:270,r:5,d:1.5},{cx:380,cy:285,r:4,d:0.8}] as b}
					<circle cx={b.cx} cy={b.cy} r={b.r} fill="none" stroke="rgba(255,255,255,0.5)" stroke-width="1.5"
						style="animation:bubble-rise 3s ease-out {b.d}s infinite"/>
				{/each}
			</svg>
		</div>

	<!-- ──────────────── MAESTROS ──────────────── -->
	{:else if world === 'maestros'}
		<div class="wb-layer wb-l1" style="transform:translateX({p1x}px)">
			<svg viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice">
				<defs>
					<linearGradient id="night-m" x1="0" y1="0" x2="0" y2="1">
						<stop offset="0%" stop-color="#1A237E"/>
						<stop offset="60%" stop-color="#311B92"/>
						<stop offset="100%" stop-color="#4527A0"/>
					</linearGradient>
				</defs>
				<rect width="400" height="200" fill="url(#night-m)"/>
				<!-- Estrellas -->
				{#each [{x:30,y:20},{x:80,y:30},{x:150,y:15},{x:220,y:25},{x:290,y:18},{x:350,y:28},{x:100,y:8},{x:250,y:10}] as st}
					<circle cx={st.x} cy={st.y} r="1.8" fill="#FFD700" opacity="0.9"/>
				{/each}
				<!-- Luna -->
				<circle cx="50" cy="38" r="22" fill="#FFF9C4" opacity="0.95"/>
				<circle cx="61" cy="32" r="17" fill="#4527A0" opacity="0.9"/>
			</svg>
		</div>
		<!-- Ciudad silueta -->
		<div class="wb-layer wb-l2" style="transform:translateX({p2x}px)">
			<svg viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice">
				<!-- Edificios: rectángulos escalonados -->
				{#each [{x:0,w:40,h:80},{x:50,w:30,h:100},{x:85,w:45,h:70},{x:140,w:35,h:90},{x:185,w:50,h:110},{x:245,w:30,h:75},{x:285,w:40,h:95},{x:335,w:35,h:85},{x:375,w:25,h:60}] as b}
					<rect x={b.x} y={200-b.h} width={b.w} height={b.h} fill="#1A237E" opacity="0.85"/>
					<!-- Ventanas -->
					{#each Array(Math.floor(b.h / 20) - 1) as _, wi}
						<rect x={b.x + b.w * 0.25} y={200 - b.h + 10 + wi * 20} width={b.w * 0.2} height="8" fill="#FFD700" opacity="0.7"/>
						<rect x={b.x + b.w * 0.6}  y={200 - b.h + 10 + wi * 20} width={b.w * 0.2} height="8" fill="#FFD700" opacity="0.5"/>
					{/each}
				{/each}
			</svg>
		</div>
		<!-- Globos aerostáticos -->
		<div class="wb-layer wb-l3" style="transform:translateX({p3x}px)">
			<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
				{#each [{cx:80,cy:200,c:'#FF6B6B',d:0},{cx:220,cy:240,c:'#FFD700',d:1.2},{cx:330,cy:210,c:'#6BCB77',d:0.6}] as g}
					<g style="animation:balloon-rise 6s ease-in-out {g.d}s infinite alternate">
						<ellipse cx={g.cx} cy={g.cy} rx="22" ry="28" fill={g.c} opacity="0.85"/>
						<path d="M{g.cx-8},{g.cy+20} L{g.cx-4},{g.cy+38} L{g.cx+4},{g.cy+38} L{g.cx+8},{g.cy+20}" fill={g.c} opacity="0.6"/>
						<line x1={g.cx-4} y1={g.cy+38} x2={g.cx-8} y2={g.cy+46} stroke="#888" stroke-width="1"/>
						<line x1={g.cx+4} y1={g.cy+38} x2={g.cx+8} y2={g.cy+46} stroke="#888" stroke-width="1"/>
						<rect x={g.cx-12} y={g.cy+42} width="20" height="10" rx="3" fill="#795548" opacity="0.8"/>
					</g>
				{/each}
			</svg>
		</div>
		<div class="wb-layer wb-l4" style="transform:translateX({p4x}px)"></div>
	{/if}
</div>

<style>
	.world-bg {
		position: fixed;
		inset: 0;
		z-index: 0;
		pointer-events: none;
		overflow: hidden;
	}
	.wb-layer {
		position: absolute;
		inset: 0;
		will-change: transform;
		transition: transform 60ms linear;
	}
	.wb-layer svg {
		width: 100%;
		height: 100%;
		display: block;
	}

	/* ── Animaciones de fondo ─────────────────── */
	/* Nubes que se deslizan de derecha a izquierda en loop */
	.cloud-slow { animation: cloud-drift 120s linear infinite; }
	.cloud-fast { animation: cloud-drift  90s linear infinite; }
	@keyframes cloud-drift {
		from { transform: translateX(0); }
		to   { transform: translateX(-50%); }
	}

	/* Nieve / partículas que caen */
	:global(.world-bg) :global(.snow-fall),
	.wb-layer :global(circle[style*="snow-fall"]) {
		animation: snow-fall 4s linear infinite;
	}
	@keyframes -global-snow-fall {
		0%   { transform: translateY(0);    opacity: 0.6; }
		100% { transform: translateY(120px); opacity: 0; }
	}

	/* Olas que se mueven lateralmente */
	.wave-slow { animation: wave-move 12s linear infinite; }
	.wave-fast { animation: wave-move  8s linear infinite; }
	@keyframes wave-move {
		from { transform: translateX(0); }
		to   { transform: translateX(-50%); }
	}

	/* Burbujas que suben */
	@keyframes -global-bubble-rise {
		0%   { transform: translateY(0);    opacity: 0.6; }
		100% { transform: translateY(-120px); opacity: 0; }
	}

	/* Globos aerostáticos que oscilan suavemente */
	@keyframes -global-balloon-rise {
		from { transform: translateY(0)   rotate(-2deg); }
		to   { transform: translateY(-30px) rotate(2deg); }
	}

	/* Pájaros que vuelan */
	:global(.bird1) { animation: bird-fly 14s linear infinite; }
	:global(.bird2) { animation: bird-fly 18s linear 1.5s infinite; }
	@keyframes -global-bird-fly {
		from { transform: translateX(-200px); }
		to   { transform: translateX(600px); }
	}

	/* Ken Burns muy lento como fallback de parallax en móvil (si solo hay degradado) */
	.world-bg-static .wb-layer { animation: none !important; transition: none !important; }

	/* Cuando quiet-mode está activo, pausar todas las animaciones del fondo */
	:global(html.quiet-mode) .world-bg * { animation-play-state: paused !important; }
</style>
