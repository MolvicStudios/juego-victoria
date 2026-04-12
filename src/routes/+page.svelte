<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { profiles, activeProfileIndex, addProfile, setActiveProfile, removeProfile, ageRange } from '$lib/stores/profiles.js';
	import { AVATARS } from '$lib/data.js';
	import { beep, say } from '$lib/audio.js';

	let profileList = $state([]);
	let showCreate = $state(false);
	let newName = $state('');
	let newPingu = $state('');
	let newAvatar = $state('🦄');
	let newBirthYear = $state(new Date().getFullYear() - 4);

	profiles.subscribe(v => { profileList = v; });

	onMount(() => {
		if (profileList.length === 0) showCreate = true;
	});

	function selectProfile(idx) {
		setActiveProfile(idx);
		const p = profileList[idx];
		const range = ageRange(p.birthYear);
		beep(600, 0.15);
		say('¡Hola ' + p.name + '! ¡Vamos a jugar!');
		goto('/exploradores');
	}

	function createProfile() {
		if (!newName.trim()) { say('¡Escribe tu nombre!'); return; }
		addProfile({
			name: newName.trim(),
			avatar: newAvatar,
			pinguName: newPingu.trim() || 'Pingu',
			birthYear: newBirthYear
		});
		const idx = profileList.length - 1;
		setActiveProfile(idx);
		beep(880, 0.2);
		say('¡Bienvenido ' + newName.trim() + '!');
		newName = ''; newPingu = ''; newAvatar = '🦄';
		showCreate = false;
		goto('/exploradores');
	}

	function deleteProfile(idx) {
		if (confirm('¿Eliminar perfil de ' + profileList[idx].name + '?')) {
			removeProfile(idx);
		}
	}
</script>

<div class="scr on" style="display:flex">
	<div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:20px;padding:20px;z-index:10">
		<div class="wel-pingu" onclick={() => { beep(700, 0.2); say('¡Hola! Soy Pingu! ¡Vamos a jugar y aprender!'); }}>🐧</div>

		{#if !showCreate}
			<h1 style="font-size:1.4rem;text-align:center">¿Quién va a jugar?</h1>

			<div style="display:flex;flex-wrap:wrap;gap:14px;justify-content:center">
				{#each profileList as p, i}
					<div class="wel-card" style="width:160px;padding:16px;cursor:pointer;position:relative" onclick={() => selectProfile(i)}>
						<div style="font-size:2.5rem;text-align:center">{p.avatar}</div>
						<div style="font-weight:900;text-align:center;font-size:1rem">{p.name}</div>
						<div style="font-size:.7rem;color:var(--ink2);text-align:center">{ageRange(p.birthYear)}</div>
						<button style="position:absolute;top:6px;right:6px;background:none;border:none;font-size:.8rem;cursor:pointer;opacity:.4"
							onclick={(e) => { e.stopPropagation(); deleteProfile(i); }}>✕</button>
					</div>
				{/each}

				{#if profileList.length < 4}
					<div class="wel-card" style="width:160px;padding:16px;cursor:pointer;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:8px;opacity:.6"
						onclick={() => { showCreate = true; }}>
						<div style="font-size:2.5rem">➕</div>
						<div style="font-weight:700;font-size:.82rem">Nuevo perfil</div>
					</div>
				{/if}
			</div>
		{:else}
			<div class="wel-card" style="max-width:420px;width:90%">
				<h1 style="font-size:1.2rem;text-align:center">¡Hola! Soy Pingu 🐧</h1>
				<p style="text-align:center;font-size:.88rem;color:var(--ink2)">¡Vamos a jugar y aprender juntos!</p>

				<label class="wel-label">Elige tu avatar:</label>
				<div class="avatar-row">
					{#each AVATARS as a}
						<div class="av-btn {a === newAvatar ? 'sel' : ''}" onclick={() => { newAvatar = a; beep(600, 0.1); }}>{a}</div>
					{/each}
				</div>

				<label class="wel-label">¿Cómo te llamas?</label>
				<input class="wel-inp" type="text" placeholder="Escribe tu nombre..." maxlength="20" autocomplete="off" bind:value={newName} />

				<label class="wel-label">Nombre del pingüino <span style="color:var(--ink2)">(opcional)</span></label>
				<input class="wel-inp" type="text" placeholder="Pingu" maxlength="15" autocomplete="off" bind:value={newPingu} />

				<label class="wel-label">Año de nacimiento</label>
				<input class="wel-inp" type="number" min={new Date().getFullYear() - 12} max={new Date().getFullYear()} bind:value={newBirthYear} />

				<button class="wel-go" onclick={createProfile}>¡Empezamos! 🚀</button>

				{#if profileList.length > 0}
					<button style="padding:10px;border:none;background:none;color:var(--ink2);font-size:.82rem;cursor:pointer;font-family:'Nunito',sans-serif"
						onclick={() => { showCreate = false; }}>← Volver a perfiles</button>
				{/if}
			</div>
		{/if}

		<div style="text-align:center;padding:8px 14px 20px;font-size:.68rem;color:var(--ink2)">
			<a href="/privacy.html" style="color:var(--ink2);text-decoration:none;margin:0 8px">Privacidad</a>
			<span>·</span>
			<a href="/terms.html" style="color:var(--ink2);text-decoration:none;margin:0 8px">Términos</a>
			<span>·</span>
			<span style="margin:0 8px">© 2025 MolvicStudios</span>
		</div>
	</div>
</div>
