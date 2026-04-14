<script>
	import { onMount, onDestroy, tick } from 'svelte';
	import { goto } from '$app/navigation';
	import { get } from 'svelte/store';
	import { page } from '$app/stores';
	import { beep, say, fanfare, boo, playCorrect, playWrong, playLevelComplete } from '$lib/audio.js';
	import { getLevel, setLevel, addStars, onGameComplete, onCorrect, onWrong, getMaxLevels, getLevels, incrementSessionCompleted, getStars, getStreak, checkNewMedals } from '$lib/stores/progress.js';
	import { profiles, activeProfileIndex, worldForAge } from '$lib/stores/profiles.js';
	import { LEVEL_COLORS, STICKER_MILESTONES } from '$lib/data.js';
	import { quietMode } from '$lib/stores/accessibility.js';
	import ParticleEngine from '$lib/effects/ParticleEngine.svelte';
	import { trigger as triggerParticle } from '$lib/effects/particleEvents.js';
	import PinguCharacter from '$lib/components/PinguCharacter.svelte';
	import { t } from '$lib/i18n/index.js';

	function getBackRoute() {
		const idx = get(activeProfileIndex);
		const profs = get(profiles);
		if (idx >= 0 && idx < profs.length) return '/' + worldForAge(profs[idx].birthYear);
		return '/';
	}

	/** Obtiene el worldId de la URL actual (ej: /nubecitas/g1 → "nubecitas") */
	function getWorldTheme() {
		const path = get(page).url.pathname;
		const match = /\/(nubecitas|exploradores|aventureros|maestros)/.exec(path);
		return match ? match[1] : 'nubecitas';
	}

	/** @type {{gameNum: number, title: string, icon: string, initGame: (container: HTMLDivElement, level: number) => void}} */
	let { gameNum, title, icon, initGame } = $props();

	/** @type {HTMLDivElement|null} */
	let container = $state(null);
	let showLevelSelect = $state(true);
	let currentLevel = $state(1);
	let celebrationVisible = $state(false);
	let celMsg = $state('');
	let celStars = $state(2);
	let celLvMsg = $state('');
	/** @type {Function|null} */
	let celCallback = $state(null);
	/** @type {any[]} */
	let confettiEls = $state([]);
	/** @type {{img:string, e:string, s:number}|null} */
	let stickerUnlock = $state(null);
	let wiggling = $state(false);
	let streak = $state(0);
	/** @type {Array<{id:string, label:string, desc:string, icon:string}>} */
	let medalQueue = $state([]);
	/** @type {{id:string, label:string, desc:string, icon:string}|null} */
	let medalUnlock = $state(null);

	// v3: estado de Pingu y modo silencioso
	/** @type {'idle'|'waiting'|'correct'|'wrong'|'excited'|'idle-long'} */
	let pinguState = $state('idle');
	let isQuiet = $state(false);
	quietMode.subscribe(v => { isQuiet = v; });
	/** @type {ReturnType<typeof setTimeout>|null} */
	let pinguStateTimer = $state(null);
	/** @type {ReturnType<typeof setTimeout>|null} */
	let idleLongTimer = $state(null);

	/**
	 * Cambia el estado de Pingu durante `ms` ms y luego vuelve a idle.
	 * Si ms es 0, el estado persiste indefinidamente.
	 * @param {'idle'|'waiting'|'correct'|'wrong'|'excited'|'idle-long'} s
	 * @param {number} ms
	 */
	function setPinguState(s, ms = 0) {
		if (pinguStateTimer) clearTimeout(pinguStateTimer);
		pinguState = s;
		if (ms > 0) {
			pinguStateTimer = setTimeout(() => { pinguState = 'idle'; }, ms);
		}
	}

	/** Reinicia el temporizador de idle-long (12s sin interacción) */
	function resetIdleLong() {
		if (idleLongTimer) clearTimeout(idleLongTimer);
		idleLongTimer = setTimeout(() => {
			if (pinguState === 'idle') setPinguState('idle-long', 2000);
		}, 12000);
	}

	function _queueMedals(/** @type {Array<{id:string, label:string, desc:string, icon:string}>} */ medals) {
		if (medals.length === 0) return;
		medalQueue = [...medalQueue, ...medals];
		if (!celebrationVisible && !medalUnlock && !stickerUnlock) {
			medalUnlock = medalQueue[0];
			medalQueue = medalQueue.slice(1);
		}
	}
	function dismissMedal() {
		if (medalQueue.length > 0) {
			medalUnlock = medalQueue[0];
			medalQueue = medalQueue.slice(1);
		} else {
			medalUnlock = null;
		}
	}

	const maxLevels = $derived.by(() => getMaxLevels());
	const levels = $derived.by(() => getLevels());

	function getMaxUnlocked() {
		const ml = getMaxLevels();
		const cl = getLevels();
		return Math.max(ml[gameNum] || 1, cl[gameNum] || 1);
	}

	onMount(() => {
		currentLevel = getLevel(gameNum);
		resetIdleLong();
		// Reiniciar idle-long en cualquier interacción del usuario
		document.addEventListener('pointerdown', resetIdleLong, { passive: true });

		// Bridge functions for vanilla JS games
		window.ppCelebrate = (/** @type {string} */ msg, stars = 2, cb = null, lvMsg = null) => {
			const starsBefore = getStars();
			celMsg = msg;
			celStars = Math.min(Math.max(stars, 1), 3);
			celLvMsg = lvMsg || '';
			celCallback = cb;
			celebrationVisible = true;
			addStars(celStars);
			const starsAfter = getStars();
			// Detectar si se cruzó un hito de sticker
			const hit = /** @type {any} */ (STICKER_MILESTONES).find(
				(/** @type {any} */ m) => m.s > starsBefore && m.s <= starsAfter
			);
			if (hit) stickerUnlock = hit;
			if (!cb) incrementSessionCompleted();
			// Check star-based and game-count medals
			_queueMedals(checkNewMedals(gameNum));
			fanfare();
			playLevelComplete();
			say(msg);
			spawnConfetti();
			// Partículas de nivel completado
			triggerParticle('levelComplete', window.innerWidth / 2, 0, getWorldTheme());
			setPinguState('correct', 700);
		};
		window.ppBeep = /** @type {any} */ (beep);
		window.ppSay = say;
		window.ppBoo = boo;
		// Exponer función de traducción global para que los juegos puedan usarla
		window.ppT = (/** @type {string} */ key, /** @type {Record<string, string|number>=} */ vars) => get(t)(key, vars);
		window.ppWin = () => {
			const msg = onGameComplete(gameNum);
			streak = 0;
			currentLevel = getLevel(gameNum);
			_queueMedals(checkNewMedals(gameNum));
			return msg;
		};
		window.ppGetLevel = () => getLevel(gameNum);
		window.ppOnCorrect = (/** @type {Event=} */ sourceEvent) => {
			onCorrect(gameNum);
			streak = getStreak(gameNum);
			_queueMedals(checkNewMedals(gameNum));
			// Feedback visual + sonido v3
			playCorrect();
			resetIdleLong();
			const world = getWorldTheme();
			// Obtener posición del elemento origen si se pasa el evento
			let px = window.innerWidth / 2, py = window.innerHeight / 2;
			if (sourceEvent && sourceEvent instanceof MouseEvent) {
				px = sourceEvent.clientX; py = sourceEvent.clientY;
			} else if (sourceEvent && /** @type {any} */ (sourceEvent).changedTouches) {
				const t = /** @type {TouchEvent} */ (sourceEvent).changedTouches[0];
				px = t.clientX; py = t.clientY;
			}
			triggerParticle('correct', px, py, world);
			// Estado Pingu según racha
			if (streak >= 3) {
				setPinguState('excited', 0); // persiste hasta siguiente evento
			} else {
				setPinguState('correct', 650);
			}
		};
		window.ppOnWrong = (/** @type {Event=} */ sourceEvent) => {
			const msg = onWrong(gameNum);
			streak = 0;
			// Dispara animación wiggle en el contenedor del juego
			if (!wiggling) {
				wiggling = true;
				setTimeout(() => { wiggling = false; }, 500);
			}
			// Feedback visual + sonido v3
			playWrong();
			resetIdleLong();
			const world = getWorldTheme();
			let px = window.innerWidth / 2, py = window.innerHeight / 2;
			if (sourceEvent && sourceEvent instanceof MouseEvent) {
				px = sourceEvent.clientX; py = sourceEvent.clientY;
			} else if (sourceEvent && /** @type {any} */ (sourceEvent).changedTouches) {
				const t = /** @type {TouchEvent} */ (sourceEvent).changedTouches[0];
				px = t.clientX; py = t.clientY;
			}
			triggerParticle('wrong', px, py, world);
			setPinguState('wrong', 550);
			return msg;
		};
	});

	onDestroy(() => {
		if (pinguStateTimer) clearTimeout(pinguStateTimer);
		if (idleLongTimer) clearTimeout(idleLongTimer);
		if (typeof window !== 'undefined') {
			document.removeEventListener('pointerdown', resetIdleLong);
			const w = /** @type {any} */ (window);
			delete w.ppCelebrate;
			delete w.ppBeep;
			delete w.ppSay;
			delete w.ppT;
			delete w.ppBoo;
			delete w.ppWin;
			delete w.ppGetLevel;
			delete w.ppOnCorrect;
			delete w.ppOnWrong;
		}
	});

	/** @param {number} lv */
	async function selectLevel(lv) {
		setLevel(gameNum, lv);
		currentLevel = lv;
		streak = 0;
		showLevelSelect = false;
		await tick();
		if (initGame && container) {
			initGame(container, lv);
		}
	}

	function celNext() {
		celebrationVisible = false;
		confettiEls = [];
		currentLevel = getLevel(gameNum);
		// Show any pending medals/stickers after celebration closes
		if (medalQueue.length > 0 && !medalUnlock) {
			medalUnlock = medalQueue[0];
			medalQueue = medalQueue.slice(1);
		}
		if (celCallback) {
			celCallback();
		} else {
			goto(getBackRoute());
		}
	}

	function goBack() {
		speechSynthesis?.cancel();
		goto(getBackRoute());
	}

	function spawnConfetti() {
		const cols = ['#FF6B6B','#FF9F43','#FFD93D','#6BCB77','#4D9FEC','#A78BFA','#F472B6'];
		const shapes = ['50%','3px','40% 0 40% 40%'];
		const items = [];
		for (let i = 0; i < 60; i++) {
			items.push({
				id: i,
				left: Math.random() * 100,
				size: 7 + Math.random() * 10,
				color: cols[Math.floor(Math.random() * cols.length)],
				radius: shapes[Math.floor(Math.random() * shapes.length)],
				delay: Math.random() * 0.6,
				dur: 2 + Math.random() * 1.2,
			});
		}
		confettiEls = items;
		setTimeout(() => { confettiEls = []; }, 3500);
	}
</script>

{#if showLevelSelect}
	<div class="lvl-select-overlay">
		<div class="lvl-select-title">{icon} {$t('ui.game.level_select_title', { title })}</div>
		<div class="lvl-select-grid">
			{#each Array(15) as _, i}
				{@const lv = i + 1}
				{@const unlocked = lv <= getMaxUnlocked()}
				{@const isCurrent = lv === currentLevel}
				<button
					class="lvl-btn {unlocked ? 'unlocked' : 'locked'} {isCurrent ? 'current' : ''}"
					style={unlocked ? `background:${LEVEL_COLORS[i]}` : ''}
					disabled={!unlocked}
					onclick={() => selectLevel(lv)}
				>
					{#if !unlocked}
						🔒<small>{lv}</small>
					{:else if lv < currentLevel}
						{lv}<small>✓</small>
					{:else if isCurrent}
						{lv}<small>⭐</small>
					{:else}
						{lv}
					{/if}
				</button>
			{/each}
		</div>
		<button class="lvl-back" onclick={goBack}>{$t('ui.game.back_menu')}</button>
	</div>
{:else}
	<div class="scr on" style="display:flex">
		<div class="hdr">
			<button class="bk" onclick={goBack}>{$t('ui.game.back')}</button>
			<!-- Pingu compañero activo v3 — muestra el estado según eventos del juego -->
			<PinguCharacter
				state={pinguState}
				size={44}
				worldTheme={getWorldTheme()}
			/>
			<span class="htl">{icon} {title}</span>
			{#if streak >= 3}
				<span class="streak-badge">🔥×{streak}</span>
			{/if}
			<span class="lvbdg">{$t('ui.game.level', { n: currentLevel })}</span>
			<!-- Toggle Modo Silencioso v3 -->
			<button
				class="quiet-toggle"
				onclick={() => quietMode.update(v => !v)}
				aria-label={isQuiet ? 'Modo silencioso activo: reactivar animaciones' : 'Modo silencioso: reduce animaciones y efectos'}
				title={isQuiet ? 'Animaciones activadas' : 'Modo silencioso'}
			>
				{isQuiet ? '☀️' : '🌙'}
			</button>
		</div>
		<div class="gbody {wiggling ? 'wiggle' : ''}" bind:this={container}></div>
	</div>
{/if}

<!-- Motor de partículas v3 — siempre montado para recibir efectos -->
<ParticleEngine />

{#if celebrationVisible}
	<div class="cel-overlay on" id="cel">
		<img class="cel-pingu" src="/assets/characters/pingu-happy.png" alt="Pingu feliz" />
		<div class="cel-msg">{celMsg}</div>
		<div class="cel-stars">
			{#each Array(celStars) as _, i}
				<img class="cstar" src="/assets/ui/star-filled.png" alt="estrella" style="animation-delay:{i * 0.15}s" />
			{/each}
		</div>
		{#if celLvMsg}
			<div class="cel-lv">{celLvMsg}</div>
		{/if}
		<button class="cel-btn" onclick={celNext}>
			{celCallback ? $t('ui.game.continue_btn') : $t('ui.game.menu_home')}
		</button>
	</div>
{/if}

{#if stickerUnlock}
	<!-- svelte-ignore a11y_no_static_element_interactions -->
	<div class="stk-popup-overlay" role="button" tabindex="0"
		onclick={() => { stickerUnlock = null; }}
		onkeydown={(e) => { if (e.key === 'Enter' || e.key === ' ' || e.key === 'Escape') stickerUnlock = null; }}>
		<div class="stk-popup" onclick={(e) => e.stopPropagation()} onkeydown={(e) => e.stopPropagation()}>
			<div class="stk-popup-title">{$t('ui.game.new_sticker')}</div>
			<img class="stk-popup-img" src="/assets/stickers/{stickerUnlock.img}" alt={stickerUnlock.e} />
			<div class="stk-popup-stars">{$t('ui.game.stars_reached', { n: stickerUnlock.s })}</div>
			<button class="stk-popup-btn" onclick={() => { stickerUnlock = null; }}>{$t('ui.game.great_sticker')}</button>
		</div>
	</div>
{/if}

{#each confettiEls as c (c.id)}
	<div class="confetti" style="left:{c.left}vw;top:-20px;width:{c.size}px;height:{c.size}px;background:{c.color};border-radius:{c.radius};animation-delay:{c.delay}s;animation-duration:{c.dur}s"></div>
{/each}

{#if medalUnlock}
	<!-- svelte-ignore a11y_no_static_element_interactions -->
	<div class="medal-overlay" role="button" tabindex="0"
		onclick={dismissMedal}
		onkeydown={(e) => { if (e.key === 'Enter' || e.key === ' ' || e.key === 'Escape') dismissMedal(); }}>
		<div class="medal-box" onclick={(e) => e.stopPropagation()} onkeydown={(e) => e.stopPropagation()}>
			<div class="medal-icon">{medalUnlock.icon}</div>
			<div class="medal-title">{$t('medals.' + medalUnlock.id + '.label')}</div>
			<div class="medal-desc">{$t('medals.' + medalUnlock.id + '.desc')}</div>
			<button class="medal-btn" onclick={dismissMedal}>{$t('ui.game.great_medal')}</button>
		</div>
	</div>
{/if}
