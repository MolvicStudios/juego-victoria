<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { profiles, activeProfileIndex, addProfile, setActiveProfile, removeProfile, ageRange, worldForAge } from '$lib/stores/profiles.js';
	import { AVATARS } from '$lib/data.js';
	import { beep, say } from '$lib/audio.js';

	// Age groups for the visual selector when creating profile
	const AGE_GROUPS = [
		{ label: '0 – 2 años', emoji: '☁️', world: 'nubecitas',   color: '#A78BFA', years: [0,1,2] },
		{ label: '3 – 5 años', emoji: '🌏', world: 'exploradores', color: '#4D9FEC', years: [3,4,5] },
		{ label: '6 – 8 años', emoji: '⚔️', world: 'aventureros',  color: '#6BCB77', years: [6,7,8] },
		{ label: '9 – 12 años',emoji: '🏆', world: 'maestros',     color: '#FF9F43', years: [9,10,11,12] },
	];

	// World metadata used on profile cards
	/** @type {Record<string, {emoji: string, color: string, label: string}>} */
	const WORLD_META = {
		nubecitas:   { emoji: '☁️', color: '#A78BFA', label: 'Nubecitas'   },
		exploradores:{ emoji: '🌏', color: '#4D9FEC', label: 'Exploradores' },
		aventureros: { emoji: '⚔️', color: '#6BCB77', label: 'Aventureros'  },
		maestros:    { emoji: '🏆', color: '#FF9F43', label: 'Maestros'     },
	};

	/** @type {any[]} */
	let profileList = $state([]);
	let showCreate = $state(false);
	let newName    = $state('');
	let newPingu   = $state('');
	let newAvatar  = $state('av-unicornio.png');
	/** @type {number|null} */
	let selectedAge = $state(null);
	let confirmDelete = $state(-1);

	profiles.subscribe(v => { profileList = v; });

	onMount(() => {
		if (profileList.length === 0) showCreate = true;
		say('¡Hola! ¿Quién va a jugar hoy?');
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
		say('¡Hola ' + p.name + '! ¡Vamos a jugar!');
		const world = worldForAge(p.birthYear);
		goto('/' + world);
	}

	function createProfile() {
		if (!newName.trim()) { say('¡Escribe tu nombre!'); return; }
		if (selectedAge === null) { say('¡Elige tu grupo de edad!'); return; }
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
		say('¡Bienvenido ' + newName.trim() + '!');
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

		<!-- Header with Padres button -->
		<div class="home-header">
			<span class="home-logo"><img src="/assets/characters/pingu-main.png" alt="Pingu" style="width:2rem;height:2rem;vertical-align:middle;margin-right:4px" /> PinguPlay</span>
			<a href="/padres" class="padres-btn">👨‍👩‍👧 Padres</a>
		</div>

		{#if !showCreate}
			<!-- Profile selector -->
			<button class="wel-pingu" onclick={() => { beep(700, 0.2); say('¡Hola! ¡Soy Pingu! ¡Vamos a jugar y aprender!'); }}>
				<img src="/assets/characters/pingu-main.png" alt="Pingu" />
			</button>
			<h1 class="home-title">¿Quién va a jugar?</h1>

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
							{meta.emoji} {meta.label}
						</div>
						{#if confirmDelete === i}
							<!-- svelte-ignore a11y_no_static_element_interactions -->
							<div class="profile-del-confirm" onclick={(e) => e.stopPropagation()} onkeydown={(e) => e.stopPropagation()}>
								<button onclick={() => confirmDeleteProfile(i)}>🗑️ Borrar</button>
								<button onclick={() => confirmDelete = -1}>✕ No</button>
							</div>
						{:else}
							<button class="profile-x" onclick={(e) => { e.stopPropagation(); deleteProfile(i); }}>✕</button>
						{/if}
					</div>
				{/each}

				{#if profileList.length < 4}
				<button type="button" class="profile-card profile-add" onclick={() => { showCreate = true; selectedAge = null; }}>
						<div style="font-size:2.8rem">➕</div>
					<div style="font-weight:700;font-size:.85rem;margin-top:6px">Nuevo perfil</div>
				</button>
				{/if}
			</div>

		{:else}
			<!-- Create profile -->
			<div class="wel-card" style="max-width:440px;width:94%">
				<h1 style="font-size:1.2rem;text-align:center">¡Crea tu perfil! 🐧</h1>

				<span class="wel-label">Elige tu avatar:</span>
				<div class="avatar-row">
					{#each AVATARS as a}
						<button class="av-btn {a.img === newAvatar ? 'sel' : ''}" onclick={() => { newAvatar = a.img; beep(600, 0.1); }}>
							<img src="/assets/avatars/{a.img}" alt={a.emoji} />
						</button>
					{/each}
				</div>

				<span class="wel-label">¿Cómo te llamas? *</span>
				<input class="wel-inp" type="text" placeholder="Escribe tu nombre..." maxlength="20" autocomplete="off" bind:value={newName} />

				<span class="wel-label">Nombre del pinguino <span style="color:var(--ink2)">(opcional)</span></span>
				<input class="wel-inp" type="text" placeholder="Pingu" maxlength="15" autocomplete="off" bind:value={newPingu} />

				<span class="wel-label">¿Cuántos años tienes? *</span>
				<div class="age-selector">
					{#each AGE_GROUPS as g, i}
						<button class="age-btn {selectedAge === i ? 'sel' : ''}"
							style="--ac:{g.color}"
							onclick={() => { selectedAge = i; beep(500, 0.1); }}>
							<span class="age-emoji">{g.emoji}</span>
							<span class="age-label">{g.label}</span>
						</button>
					{/each}
				</div>

				<button class="wel-go" onclick={createProfile}>¡Empezamos! 🚀</button>

				{#if profileList.length > 0}
					<button class="wel-back" onclick={() => { showCreate = false; }}>← Volver</button>
				{/if}
			</div>
		{/if}

		<div class="home-footer">
			<a href="/privacy.html">Privacidad</a>
			<span>·</span>
			<a href="/terms.html">Términos</a>
			<span>·</span>
			<span>© 2026 MolvicStudios</span>
		</div>
	</div>
</div>
