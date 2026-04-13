<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { profiles, activeProfileIndex } from '$lib/stores/profiles.js';
	import { getStars, getLevels, getSessionData, getUnlockedMedals } from '$lib/stores/progress.js';
	import { night, hiContrast, bigText } from '$lib/stores/settings.js';
	import { GAMES, STICKER_MILESTONES, MEDALS } from '$lib/data.js';
	import { beep, say, fanfare } from '$lib/audio.js';
	import WorldBackground from '$lib/backgrounds/WorldBackground.svelte';

	/**
	 * @prop {string}   worldId    - 'nubecitas' | 'exploradores' | 'aventureros' | 'maestros'
	 * @prop {string}   worldEmoji
	 * @prop {string}   worldLabel
	 * @prop {string}   worldColor  - hex
	 * @prop {number[]} gameNums   - which game numbers to show
	 */
	let { worldId, worldEmoji, worldLabel, worldColor, gameNums } = $props();

	/** @type {any} */
	let profile   = $state(null);
	let stars     = $state(0);
	/** @type {Record<number, number>} */
	let levels    = $state({});
	let isNight   = $state(false);
	let showStickers = $state(false);
	let showSummary  = $state(false);
	let showSettings = $state(false);
	let showTutorial = $state(false);
	let tutStep      = $state(0);
	let isHiContrast = $state(false);
	let isBigText    = $state(false);
	/** @type {string[]} */
	let unlockedMedals = $state([]);

	const TUTORIAL_STEPS = [
		{ img: '/assets/characters/pingu-main.png', title: '¡Bienvenido a PinguPlay!', body: 'Soy Pingu, tu compañero de aprendizaje 🐧' },
		{ img: '/assets/characters/pingu-happy.png', title: '¡Elige un juego!', body: 'Toca cualquier tarjeta para empezar a aprender 🎮' },
		{ img: '/assets/characters/pingu-happy.png', title: '¡Gana Estrellas ⭐!', body: 'Cada respuesta correcta da estrellas. ¡Desbloquea stickers y medallas!' },
	];

	hiContrast.subscribe(v => { isHiContrast = v; });
	bigText.subscribe(v => { isBigText = v; });
	night.subscribe(v => { isNight = v; });

	/** Games filtered and ordered for this world */
	const worldGames = $derived(GAMES.filter(g => gameNums.includes(g.n)));

	onMount(() => {
		let idxVal = -1;
		activeProfileIndex.subscribe(v => { idxVal = v; });
		profiles.subscribe(arr => {
			if (idxVal >= 0 && idxVal < arr.length) {
				profile = arr[idxVal];
			} else {
				goto('/');
			}
		});
		refreshData();
		const sess = getSessionData();
		if (sess.sessionCompleted >= 6) {
			showSummary = true;
			fanfare();
			say('¡Qué bien lo has hecho hoy!');
		}
		say('¡Hola! ¡Elige un juego!');
		if (!localStorage.getItem('pp_tut')) showTutorial = true;
	});

	function refreshData() {
		stars  = getStars();
		levels = getLevels();
	}

	/** @param {number} n */
	function goGame(n) {
		speechSynthesis?.cancel();
		goto(`/${worldId}/g${n}`);
	}

	function toggleNightMode() {
		night.update(v => !v);
		beep(500, 0.1);
	}

	function openStickers() {
		refreshData();
		unlockedMedals = getUnlockedMedals();
		showStickers = true;
	}

	function advanceTutorial() {
		if (tutStep < TUTORIAL_STEPS.length - 1) {
			tutStep++;
		} else {
			localStorage.setItem('pp_tut', '1');
			showTutorial = false;
		}
	}
	function skipTutorial() {
		localStorage.setItem('pp_tut', '1');
		showTutorial = false;
	}
</script>

{#if showSummary}
	<div class="scr on" style="display:flex">
		<img class="sum-pingu" src="/assets/characters/pingu-happy.png" alt="Pingu feliz" />
		<div class="sum-card">
			<h2>¡Sesión increíble, {profile?.name || ''}!</h2>
			<div class="sum-stars">Ganaste ⭐ {getSessionData().sessionStars} estrellas hoy</div>
			<div style="font-size:.82rem;color:var(--ink2)">Jugaste {getSessionData().sessionCompleted} juegos 🎮</div>
			<div class="sum-btns">
				<button class="sum-btn" style="background:var(--c4);color:#fff" onclick={() => { showSummary = false; }}>¡Seguir jugando!</button>
				<button class="sum-btn" style="background:#EEE;color:var(--ink)" onclick={() => goto('/')}>Salir</button>
			</div>
		</div>
	</div>
{:else}
	<div class="scr on" style="display:flex">
		<!-- Fondo parallax v3 -->
		<WorldBackground world={worldId} interactive={true} />
		<div class="men-top" style="background:linear-gradient(135deg,{worldColor}22 0%,{worldColor}08 100%)">
			{#if profile?.avatar?.endsWith('.png')}
				<img class="men-avatar" src="/assets/avatars/{profile.avatar}" alt={profile.name} style="border:3px solid {worldColor}" />
			{:else}
				<span class="men-avatar" style="border:3px solid {worldColor}40">{profile?.avatar || '🦄'}</span>
			{/if}
			<div class="men-info">
				<h2 style="font-size:var(--text-lg)">¡Hola, {profile?.name || ''}!</h2>
				<div class="world-badge" style="background:{worldColor}">{worldEmoji} {worldLabel}</div>
			</div>
			<div class="men-btns">
				<button class="men-pill" onclick={toggleNightMode}><span>{isNight ? '☀️' : '🌙'}</span></button>
				<button class="men-pill" onclick={openStickers}>🏆 <span>{stars}</span></button>
				<button class="men-pill" onclick={() => { showSettings = true; }}>⚙️</button>
			</div>
		</div>

		<div class="mgrid">
			{#each worldGames as gm, idx}
				<button class="mcard" data-new={gm.isNew ? 'true' : 'false'} style="animation-delay:{idx * 0.04}s;--col:{gm.col}" onclick={() => goGame(gm.n)}>

				<img class="ico" src="/assets/games/{gm.img}" alt={gm.name} />
					<h3>{gm.name}</h3>
					<small>{gm.sub}</small>
					<span class="mlv">Nv.{levels[gm.n] || 1}</span>
					{#if gm.isNew}
						<span class="new-badge">NUEVO</span>
					{/if}
				</button>
			{/each}
		</div>

		<div class="home-footer" style="padding-bottom:72px">
			<a href="/privacy.html">Privacidad</a>
			<span>·</span>
			<a href="/terms.html">Términos</a>
			<span>·</span>
			<a href="/padres">👨‍👩‍👧 Padres</a>
		</div>
	</div>
{/if}

{#if showSettings}
	<!-- svelte-ignore a11y_no_static_element_interactions -->
	<div class="modal-overlay on" role="button" tabindex="0"
		onclick={() => { showSettings = false; }}
		onkeydown={(e) => { if(e.key==='Escape') showSettings = false; }}>
		<!-- svelte-ignore a11y_no_static_element_interactions a11y_no_noninteractive_element_interactions -->
		<div class="modal-box settings-box" onclick={(e) => e.stopPropagation()} onkeydown={(e) => e.stopPropagation()}>
			<h2>⚙️ Ajustes</h2>
			<div class="setting-row">
				<span>🌙 Modo nocturno</span>
				<button class="toggle-btn {isNight ? 'on' : ''}" onclick={toggleNightMode}>{isNight ? 'ON' : 'OFF'}</button>
			</div>
			<div class="setting-row">
				<span>🔍 Texto grande</span>
				<button class="toggle-btn {isBigText ? 'on' : ''}" onclick={() => bigText.update(v => !v)}>{isBigText ? 'ON' : 'OFF'}</button>
			</div>
			<div class="setting-row">
				<span>⬛ Alto contraste</span>
				<button class="toggle-btn {isHiContrast ? 'on' : ''}" onclick={() => hiContrast.update(v => !v)}>{isHiContrast ? 'ON' : 'OFF'}</button>
			</div>
			<button class="modal-close" onclick={() => { showSettings = false; }}>Cerrar</button>
		</div>
	</div>
{/if}

{#if showTutorial}
	<div class="tut-overlay">
		<div class="tut-card">
			<img class="tut-pingu" src={TUTORIAL_STEPS[tutStep].img} alt="Pingu" />
			<h2 class="tut-title">{TUTORIAL_STEPS[tutStep].title}</h2>
			<p class="tut-body">{TUTORIAL_STEPS[tutStep].body}</p>
			<div class="tut-dots">
				{#each TUTORIAL_STEPS as _, i}
					<span class="tut-dot {tutStep === i ? 'active' : ''}"></span>
				{/each}
			</div>
			<button class="tut-next" onclick={advanceTutorial}>
				{tutStep < TUTORIAL_STEPS.length - 1 ? 'Siguiente →' : '¡Empezar! 🚀'}
			</button>
			<button class="tut-skip" onclick={skipTutorial}>Saltar tutorial</button>
		</div>
	</div>
{/if}

{#if showStickers}
	<!-- svelte-ignore a11y_no_static_element_interactions -->
	<div class="modal-overlay on" role="button" tabindex="0"
		onclick={() => { showStickers = false; }}
		onkeydown={(e) => { if(e.key==='Escape'||e.key==='Enter') showStickers = false; }}>
		<!-- svelte-ignore a11y_no_static_element_interactions a11y_no_noninteractive_element_interactions -->
		<div class="modal-box" onclick={(e) => e.stopPropagation()} onkeydown={(e) => e.stopPropagation()}>
			<h2>🏆 Mi Colección</h2>
			<div class="stk-grid">
				{#each STICKER_MILESTONES as m}
					{@const unlocked = stars >= m.s}
					{@const stkImg = /** @type {any} */(m).img}
					<div class="stk-item {unlocked ? 'unlocked' : 'locked'}">
					{#if unlocked}
						<img src="/assets/stickers/{stkImg}" alt={m.e} />
					{:else}
						<img class="stk-locked" src="/assets/ui/lock.png" alt="bloqueado" />
					{/if}
					<small>{m.s}⭐</small>
					</div>
				{/each}
			</div>				<h3 style="margin-top:14px;font-size:1rem">🎖️ Medallas</h3>
				<div class="medals-coll-grid">
					{#each MEDALS as m}
						{@const ul = unlockedMedals.includes(m.id)}
						<div class="medal-coll-item {ul ? 'ul' : 'lk'}">
							<span style="font-size:1.8rem;{ul ? '' : 'filter:grayscale(1);opacity:.25'}">{m.icon}</span>
							<small>{ul ? m.label : '???'}</small>
						</div>
					{/each}
				</div>			<button class="modal-close" onclick={() => { showStickers = false; }}>¡Cerrar!</button>
		</div>
	</div>
{/if}
