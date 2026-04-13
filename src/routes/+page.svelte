<script>
	import { onMount } from 'svelte';
	import { get } from 'svelte/store';
	import { goto } from '$app/navigation';
	import { profiles, activeProfileIndex, addProfile, setActiveProfile, removeProfile, ageRange, worldForAge } from '$lib/stores/profiles.js';
	import { AVATARS } from '$lib/data.js';
	import { beep, say } from '$lib/audio.js';
	import { t } from '$lib/i18n/index.js';
	import LanguageSelector from '$lib/components/LanguageSelector.svelte';

	// Age groups for the visual selector when creating profile
	const AGE_GROUPS = [
		{ key: 'ui.age.0_2', emoji: '☁️', world: 'nubecitas',   color: '#A78BFA', years: [0,1,2] },
		{ key: 'ui.age.3_5', emoji: '🌏', world: 'exploradores', color: '#4D9FEC', years: [3,4,5] },
		{ key: 'ui.age.6_8', emoji: '⚔️', world: 'aventureros',  color: '#6BCB77', years: [6,7,8] },
		{ key: 'ui.age.9_12',emoji: '🏆', world: 'maestros',     color: '#FF9F43', years: [9,10,11,12] },
	];

	// World metadata used on profile cards
	/** @type {Record<string, {emoji: string, color: string, labelKey: string}>} */
	const WORLD_META = {
		nubecitas:   { emoji: '☁️', color: '#A78BFA', labelKey: 'worlds.nubecitas.name'   },
		exploradores:{ emoji: '🌏', color: '#4D9FEC', labelKey: 'worlds.exploradores.name' },
		aventureros: { emoji: '⚔️', color: '#6BCB77', labelKey: 'worlds.aventureros.name'  },
		maestros:    { emoji: '🏆', color: '#FF9F43', labelKey: 'worlds.maestros.name'     },
	};

	/** @type {any[]} */
	let profileList = $state([]);
	let showCreate = $state(false);
	let showLangSelect = $state(false);
	let newName    = $state('');
	let newPingu   = $state('');
	let newAvatar  = $state('av-unicornio.png');
	/** @type {number|null} */
	let selectedAge = $state(null);
	let confirmDelete = $state(-1);

	profiles.subscribe(v => { profileList = v; });

	onMount(() => {
		if (profileList.length === 0) showCreate = true;
		say(get(t)('say.hello_who_plays'));
		// Show language selector on first visit (no locale saved)
		if (!localStorage.getItem('pp_locale')) showLangSelect = true;
	});

	/** @param {number} groupIdx */
	function birthYearFromGroup(groupIdx) {
		// Use middle year of selected group
		const group = AGE_GROUPS[groupIdx];
		const midAge = group.years[Math.floor(group.years.length / 2)];
		return new Date().getFullYear() - midAge;
	}

	/** @param {number} idx */
	function selectProfile(idx) {
		setActiveProfile(idx);
		const p = profileList[idx];
		beep(600, 0.15);
		say(get(t)('say.hello_name', { name: p.name }));
		const world = worldForAge(p.birthYear);
		goto('/' + world);
	}

	function createProfile() {
		if (!newName.trim()) { say(get(t)('say.write_name')); return; }
		if (selectedAge === null) { say(get(t)('say.choose_age')); return; }
		const birthYear = birthYearFromGroup(selectedAge);
		addProfile({
			name: newName.trim(),
			avatar: newAvatar,
			pinguName: newPingu.trim() || 'Pingu',
			birthYear
		});
		const idx = profileList.length - 1;
		setActiveProfile(idx);
		beep(880, 0.2);
		say(get(t)('say.welcome_name', { name: newName.trim() }));
		newName = ''; newPingu = ''; newAvatar = 'av-unicornio.png'; selectedAge = null;
		showCreate = false;
		const world = worldForAge(birthYear);
		goto('/' + world);
	}

	/** @param {number} idx */
	function deleteProfile(idx) {
		confirmDelete = confirmDelete === idx ? -1 : idx;
	}
	/** @param {number} idx */
	function confirmDeleteProfile(idx) {
		removeProfile(idx);
		confirmDelete = -1;
	}
</script>



<div class="scr on" style="display:flex">
	<div class="home-wrap">

		<!-- Language selector overlay (first visit) -->
		{#if showLangSelect}
			<div class="lang-overlay">
				<div class="lang-box">
					<img src="/assets/characters/pingu-main.png" alt="Pingu" class="lang-pingu" />
					<LanguageSelector variant="onboarding" onConfirm={() => { showLangSelect = false; }} />
				</div>
			</div>
		{/if}

		<!-- Header with Padres button -->
		<div class="home-header">
			<span class="home-logo"><img src="/assets/characters/pingu-main.png" alt="Pingu" style="width:2rem;height:2rem;vertical-align:middle;margin-right:4px" /> PinguPlay</span>
			<a href="/padres" class="padres-btn">{$t('ui.home.parents_btn')}</a>
		</div>

		{#if !showCreate}
			<!-- Profile selector -->
			<button class="wel-pingu" onclick={() => { beep(700, 0.2); say(get(t)('say.pingu_hello')); }}>
				<img src="/assets/characters/pingu-main.png" alt="Pingu" />
			</button>
			<h1 class="home-title">{$t('ui.home.who_plays')}</h1>

			<div class="profiles-grid">
				{#each profileList as p, i}
					{@const world = worldForAge(p.birthYear)}
					{@const meta = WORLD_META[world]}
					<!-- svelte-ignore a11y_no_static_element_interactions -->
					<div class="profile-card" role="button" tabindex="0"
						onclick={() => confirmDelete === i ? null : selectProfile(i)}
						onkeydown={(e) => { if(e.key==='Enter'||e.key===' ') { e.preventDefault(); if(confirmDelete !== i) selectProfile(i); } }}
						style="--pc:{meta.color}">
						<div class="profile-av">
						{#if p.avatar?.endsWith('.png')}
							<img src="/assets/avatars/{p.avatar}" alt={p.name} />
						{:else}
							{p.avatar}
						{/if}
					</div>
						<div class="profile-name">{p.name}</div>
						<div class="profile-world" style="background:{meta.color}22;color:{meta.color}">
							{meta.emoji} {$t(meta.labelKey)}
						</div>
						{#if confirmDelete === i}
							<!-- svelte-ignore a11y_no_static_element_interactions -->
							<div class="profile-del-confirm" onclick={(e) => e.stopPropagation()} onkeydown={(e) => e.stopPropagation()}>
								<button onclick={() => confirmDeleteProfile(i)}>{$t('ui.profile.delete')}</button>
								<button onclick={() => confirmDelete = -1}>{$t('ui.profile.cancel_delete')}</button>
							</div>
						{:else}
							<button class="profile-x" onclick={(e) => { e.stopPropagation(); deleteProfile(i); }}>✕</button>
						{/if}
					</div>
				{/each}

				{#if profileList.length < 4}
				<button type="button" class="profile-card profile-add" onclick={() => { showCreate = true; selectedAge = null; }}>
						<div style="font-size:2.8rem">➕</div>
					<div style="font-weight:700;font-size:.85rem;margin-top:6px">{$t('ui.home.new_profile')}</div>
				</button>
				{/if}
			</div>

		{:else}
			<!-- Create profile -->
			<div class="wel-card" style="max-width:440px;width:94%">
				<h1 style="font-size:1.2rem;text-align:center">{$t('ui.profile.create_title')}</h1>

				<span class="wel-label">{$t('ui.profile.choose_avatar')}</span>
				<div class="avatar-row">
					{#each AVATARS as a}
						<button class="av-btn {a.img === newAvatar ? 'sel' : ''}" onclick={() => { newAvatar = a.img; beep(600, 0.1); }}>
							<img src="/assets/avatars/{a.img}" alt={a.emoji} />
						</button>
					{/each}
				</div>

				<span class="wel-label">{$t('ui.profile.your_name')}</span>
				<input class="wel-inp" type="text" placeholder={$t('ui.profile.name_placeholder')} maxlength="20" autocomplete="off" bind:value={newName} />

				<span class="wel-label">{$t('ui.profile.penguin_name')} <span style="color:var(--ink2)">{$t('ui.profile.optional')}</span></span>
				<input class="wel-inp" type="text" placeholder={$t('ui.profile.penguin_placeholder')} maxlength="15" autocomplete="off" bind:value={newPingu} />

				<span class="wel-label">{$t('ui.profile.age_question')}</span>
				<div class="age-selector">
					{#each AGE_GROUPS as g, i}
						<button class="age-btn {selectedAge === i ? 'sel' : ''}"
							style="--ac:{g.color}"
							onclick={() => { selectedAge = i; beep(500, 0.1); }}>
							<span class="age-emoji">{g.emoji}</span>
							<span class="age-label">{$t(g.key)}</span>
						</button>
					{/each}
				</div>

				<button class="wel-go" onclick={createProfile}>{$t('ui.profile.start_btn')}</button>

				{#if profileList.length > 0}
					<button class="wel-back" onclick={() => { showCreate = false; }}>{$t('ui.profile.back')}</button>
				{/if}
			</div>
		{/if}

		<div class="home-footer">
			<a href="/privacy.html">{$t('ui.footer.privacy')}</a>
			<span>·</span>
			<a href="/terms.html">{$t('ui.footer.terms')}</a>
			<span>·</span>
			<span>{$t('ui.footer.copyright')}</span>
		</div>
	</div>
</div>

<style>
	.lang-overlay {
		position: fixed;
		inset: 0;
		background: rgba(0,0,0,.45);
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 1000;
	}
	.lang-box {
		background: #fff;
		border-radius: 24px;
		padding: 8px 8px 24px;
		box-shadow: 0 8px 40px rgba(0,0,0,.25);
		max-width: 360px;
		width: 94%;
		display: flex;
		flex-direction: column;
		align-items: center;
	}
	.lang-pingu {
		width: 80px;
		height: 80px;
		margin-bottom: -8px;
	}
</style>
