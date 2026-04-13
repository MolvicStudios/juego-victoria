<script>
	import { onMount } from 'svelte';
	import { get } from 'svelte/store';
	import { goto } from '$app/navigation';
	import { profiles, activeProfileIndex } from '$lib/stores/profiles.js';
	import { getStars, getLevels, getSessionData, getUnlockedMedals } from '$lib/stores/progress.js';
	import { night, hiContrast, bigText } from '$lib/stores/settings.js';
	import { GAMES, STICKER_MILESTONES, MEDALS } from '$lib/data.js';
	import { beep, say, fanfare } from '$lib/audio.js';
	import WorldBackground from '$lib/backgrounds/WorldBackground.svelte';
	import { t } from '$lib/i18n/index.js';
	import LanguageSelector from '$lib/components/LanguageSelector.svelte';

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

	const TUTORIAL_IMGS = [
		'/assets/characters/pingu-main.png',
		'/assets/characters/pingu-happy.png',
		'/assets/characters/pingu-happy.png',
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
			say(get(t)('say.great_today'));
		}
		say(get(t)('say.hello_choose_game'));
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
		if (tutStep < TUTORIAL_IMGS.length - 1) {
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
			<h2>{$t('ui.summary.title', { name: profile?.name || '' })}</h2>
			<div class="sum-stars">{$t('ui.summary.stars', { n: getSessionData().sessionStars })}</div>
			<div style="font-size:.82rem;color:var(--ink2)">{$t('ui.summary.games', { n: getSessionData().sessionCompleted })}</div>
			<div class="sum-btns">
				<button class="sum-btn" style="background:var(--c4);color:#fff" onclick={() => { showSummary = false; }}>{$t('ui.hub.keep_playing')}</button>
				<button class="sum-btn" style="background:#EEE;color:var(--ink)" onclick={() => goto('/')}>{$t('ui.hub.exit')}</button>
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
						<h2 style="font-size:var(--text-lg)">{$t('ui.hub.hello', { name: profile?.name || '' })}</h2>
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

			<img class="ico" src="/assets/games/{gm.img}" alt={$t('games.' + gm.n + '.title')} />
				<h3>{$t('games.' + gm.n + '.title')}</h3>
				<small>{$t('games.' + gm.n + '.sub')}</small>
				<span class="mlv">{$t('ui.hub.level_short', { n: levels[gm.n] || 1 })}</span>
				{#if gm.isNew}
					<span class="new-badge">{$t('ui.hub.new_badge')}</span>
					{/if}
				</button>
			{/each}
		</div>

		<div class="home-footer" style="padding-bottom:72px">
			<a href="/privacy.html">{$t('ui.footer.privacy')}</a>
			<span>·</span>
			<a href="/terms.html">{$t('ui.footer.terms')}</a>
			<span>·</span>
			<a href="/padres">{$t('ui.hub.parents_link')}</a>
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
			<h2>{$t('ui.settings.title')}</h2>
			<div class="setting-row">
				<span>{$t('ui.settings.night_mode')}</span>
				<button class="toggle-btn {isNight ? 'on' : ''}" onclick={toggleNightMode}>{isNight ? $t('ui.settings.on') : $t('ui.settings.off')}</button>
			</div>
			<div class="setting-row">
				<span>{$t('ui.settings.big_text')}</span>
				<button class="toggle-btn {isBigText ? 'on' : ''}" onclick={() => bigText.update(v => !v)}>{isBigText ? $t('ui.settings.on') : $t('ui.settings.off')}</button>
			</div>
			<div class="setting-row">
				<span>{$t('ui.settings.high_contrast')}</span>
				<button class="toggle-btn {isHiContrast ? 'on' : ''}" onclick={() => hiContrast.update(v => !v)}>{isHiContrast ? $t('ui.settings.on') : $t('ui.settings.off')}</button>
			</div>
			<div class="setting-row" style="flex-direction:column;align-items:flex-start;gap:8px">
				<span>{$t('ui.settings.language')}</span>
				<LanguageSelector variant="settings" />
			</div>
			<button class="modal-close" onclick={() => { showSettings = false; }}>{$t('ui.settings.close')}</button>
		</div>
	</div>
{/if}

{#if showTutorial}
	<div class="tut-overlay">
		<div class="tut-card">
			<img class="tut-pingu" src={TUTORIAL_IMGS[tutStep]} alt="Pingu" />
			<h2 class="tut-title">{$t('ui.tutorial.step' + tutStep + '_title')}</h2>
			<p class="tut-body">{$t('ui.tutorial.step' + tutStep + '_body')}</p>
			<div class="tut-dots">
				{#each TUTORIAL_IMGS as _, i}
					<span class="tut-dot {tutStep === i ? 'active' : ''}"></span>
				{/each}
			</div>
			<button class="tut-next" onclick={advanceTutorial}>
				{tutStep < TUTORIAL_IMGS.length - 1 ? $t('ui.tutorial.next') : $t('ui.tutorial.start')}
			</button>
			<button class="tut-skip" onclick={skipTutorial}>{$t('ui.tutorial.skip')}</button>
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
			<h2>{$t('ui.hub.collection')}</h2>
			<div class="stk-grid">
				{#each STICKER_MILESTONES as m}
					{@const unlocked = stars >= m.s}
					{@const stkImg = /** @type {any} */(m).img}
					<div class="stk-item {unlocked ? 'unlocked' : 'locked'}">
					{#if unlocked}
						<img src="/assets/stickers/{stkImg}" alt={m.e} />
					{:else}
						<img class="stk-locked" src="/assets/ui/lock.png" alt={$t('ui.hub.locked')} />
					{/if}
					<small>{m.s}⭐</small>
					</div>
				{/each}
			</div>				<h3 style="margin-top:14px;font-size:1rem">{$t('ui.hub.medals_section')}</h3>
				<div class="medals-coll-grid">
					{#each MEDALS as m}
						{@const ul = unlockedMedals.includes(m.id)}
						<div class="medal-coll-item {ul ? 'ul' : 'lk'}">
							<span style="font-size:1.8rem;{ul ? '' : 'filter:grayscale(1);opacity:.25'}">{m.icon}</span>
							<small>{ul ? $t('medals.' + m.id + '.label') : '???'}</small>
						</div>
					{/each}
				</div>			<button class="modal-close" onclick={() => { showStickers = false; }}>{$t('ui.hub.close_collection')}</button>
		</div>
	</div>
{/if}
