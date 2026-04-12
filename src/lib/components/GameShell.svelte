<script>
	import { onMount, onDestroy, tick } from 'svelte';
	import { goto } from '$app/navigation';
	import { get } from 'svelte/store';
	import { beep, say, fanfare, boo } from '$lib/audio.js';
	import { getLevel, setLevel, addStars, onGameComplete, onCorrect, onWrong, getMaxLevels, getLevels, incrementSessionCompleted } from '$lib/stores/progress.js';
	import { profiles, activeProfileIndex, worldForAge } from '$lib/stores/profiles.js';
	import { LEVEL_COLORS } from '$lib/data.js';

	function getBackRoute() {
		const idx = get(activeProfileIndex);
		const profs = get(profiles);
		if (idx >= 0 && idx < profs.length) return '/' + worldForAge(profs[idx].birthYear);
		return '/';
	}

	/** @type {{gameNum: number, title: string, icon: string, initGame: (container: HTMLDivElement, level: number) => void, children: any}} */
	let { gameNum, title, icon, initGame, children } = $props();

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

	const maxLevels = $derived.by(() => getMaxLevels());
	const levels = $derived.by(() => getLevels());

	function getMaxUnlocked() {
		const ml = getMaxLevels();
		const cl = getLevels();
		return Math.max(ml[gameNum] || 1, cl[gameNum] || 1);
	}

	onMount(() => {
		currentLevel = getLevel(gameNum);

		// Bridge functions for vanilla JS games
		window.ppCelebrate = (/** @type {string} */ msg, stars = 2, cb = null, lvMsg = null) => {
			celMsg = msg;
			celStars = Math.min(Math.max(stars, 1), 3);
			celLvMsg = lvMsg || '';
			celCallback = cb;
			celebrationVisible = true;
			addStars(celStars);
			if (!cb) incrementSessionCompleted();
			fanfare();
			say(msg);
			spawnConfetti();
		};
		window.ppBeep = /** @type {any} */ (beep);
		window.ppSay = say;
		window.ppBoo = boo;
		window.ppWin = () => {
			const msg = onGameComplete(gameNum);
			currentLevel = getLevel(gameNum);
			return msg;
		};
		window.ppGetLevel = () => getLevel(gameNum);
		window.ppOnCorrect = () => onCorrect(gameNum);
		window.ppOnWrong = () => onWrong(gameNum);
	});

	onDestroy(() => {
		if (typeof window !== 'undefined') {
			delete window.ppCelebrate;
			delete window.ppBeep;
			delete window.ppSay;
			delete window.ppBoo;
			delete window.ppWin;
			delete window.ppGetLevel;
			delete window.ppOnCorrect;
			delete window.ppOnWrong;
		}
	});

	/** @param {number} lv */
	async function selectLevel(lv) {
		setLevel(gameNum, lv);
		currentLevel = lv;
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
		<div class="lvl-select-title">{icon} {title} — Elige tu nivel</div>
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
		<button class="lvl-back" onclick={goBack}>← Volver al menú</button>
	</div>
{:else}
	<div class="scr on" style="display:flex">
		<div class="hdr">
			<button class="bk" onclick={goBack}>←</button>
			<span class="htl">{icon} {title}</span>
			<span class="lvbdg">Nivel {currentLevel}</span>
		</div>
		<div class="gbody" bind:this={container}>
			{@render children?.()}
		</div>
	</div>
{/if}

{#if celebrationVisible}
	<div class="cel-overlay on" id="cel">
		<div class="cel-pingu">🐧</div>
		<div class="cel-msg">{celMsg}</div>
		<div class="cel-stars">
			{#each Array(celStars) as _, i}
				<span class="cstar" style="animation-delay:{i * 0.15}s">⭐</span>
			{/each}
		</div>
		{#if celLvMsg}
			<div class="cel-lv">{celLvMsg}</div>
		{/if}
		<button class="cel-btn" onclick={celNext}>
			{celCallback ? '¡Seguir! →' : 'Menú 🏠'}
		</button>
	</div>
{/if}

{#each confettiEls as c (c.id)}
	<div class="confetti" style="left:{c.left}vw;top:-20px;width:{c.size}px;height:{c.size}px;background:{c.color};border-radius:{c.radius};animation-delay:{c.delay}s;animation-duration:{c.dur}s"></div>
{/each}
