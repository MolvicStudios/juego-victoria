<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { profiles, activeProfileIndex } from '$lib/stores/profiles.js';
	import { getStars, getLevels, getSessionData } from '$lib/stores/progress.js';
	import { night } from '$lib/stores/settings.js';
	import { GAMES, STICKER_MILESTONES } from '$lib/data.js';
	import { beep, say, fanfare } from '$lib/audio.js';

	/**
	 * @prop {string}   worldId    - 'nubecitas' | 'exploradores' | 'aventureros' | 'maestros'
	 * @prop {string}   worldEmoji
	 * @prop {string}   worldLabel
	 * @prop {string}   worldColor  - hex
	 * @prop {number[]} gameNums   - which game numbers to show
	 */
	let { worldId, worldEmoji, worldLabel, worldColor, gameNums } = $props();

	let profile   = $state(null);
	let stars     = $state(0);
	let levels    = $state({});
	let isNight   = $state(false);
	let showStickers = $state(false);
	let showSummary  = $state(false);

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
	});

	function refreshData() {
		stars  = getStars();
		levels = getLevels();
	}

	function goGame(n) {
		speechSynthesis?.cancel();
		// All games live under /exploradores/gN
		goto(`/exploradores/g${n}`);
	}

	function toggleNightMode() {
		night.update(v => !v);
		beep(500, 0.1);
	}

	function openStickers() {
		refreshData();
		showStickers = true;
	}
</script>

{#if showSummary}
	<div class="scr on" style="display:flex">
		<div class="sum-pingu">🐧</div>
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
		<div class="men-top">
			<span class="men-avatar">{profile?.avatar || '🦄'}</span>
			<div class="men-info">
				<h2>¡Hola, {profile?.name || ''}!</h2>
				<div class="world-badge" style="background:{worldColor}">{worldEmoji} {worldLabel}</div>
			</div>
			<div class="men-btns">
				<button class="men-pill" onclick={toggleNightMode}><span>{isNight ? '☀️' : '🌙'}</span></button>
				<button class="men-pill" onclick={openStickers}>🏆 <span>{stars}</span></button>
			</div>
		</div>

		<div class="mgrid">
			{#each worldGames as gm, idx}
				<button class="mcard" style="animation-delay:{idx * 0.04}s;--col:{gm.col}" onclick={() => goGame(gm.n)}>

					<span class="ico">{gm.ico}</span>
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

{#if showStickers}
	<div class="modal-overlay on" onclick={() => { showStickers = false; }}>
		<!-- svelte-ignore a11y_click_events_have_key_events -->
		<div class="modal-box" onclick={(e) => e.stopPropagation()}>
			<h2>🏆 Mi Colección</h2>
			<div class="stk-grid">
				{#each STICKER_MILESTONES as m}
					{@const unlocked = stars >= m.s}
					<div class="stk-item {unlocked ? 'unlocked' : 'locked'}">
						{unlocked ? m.e : '🔒'}<small>{m.s}⭐</small>
					</div>
				{/each}
			</div>
			<button class="modal-close" onclick={() => { showStickers = false; }}>¡Cerrar!</button>
		</div>
	</div>
{/if}
