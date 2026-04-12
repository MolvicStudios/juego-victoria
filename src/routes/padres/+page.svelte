<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { profiles, activeProfileIndex } from '$lib/stores/profiles.js';
	import { allProgress } from '$lib/stores/progress.js';
	import { parentPin, night, muted } from '$lib/stores/settings.js';
	import { GAMES } from '$lib/data.js';

	let authenticated = $state(false);
	let pinInput = $state('');
	let pinError = $state('');
	let activeTab = $state('stats');
	let showSetPin = $state(false);
	let newPin = $state('');

	function checkPin() {
		const stored = $parentPin;
		if (!stored) { authenticated = true; return; }
		if (pinInput === stored) { authenticated = true; pinError = ''; }
		else { pinError = 'PIN incorrecto'; pinInput = ''; }
	}

	function savePin() {
		if (newPin.length === 4 && /^\d{4}$/.test(newPin)) {
			$parentPin = newPin;
			showSetPin = false; newPin = '';
		}
	}

	function removePin() { $parentPin = ''; }

	function getProfileProgress(idx) {
		const key = 'p' + idx;
		const prog = $allProgress[key] || {};
		let totalStars = 0, gamesPlayed = 0, maxLevel = 0;
		for (const g of GAMES) {
			const gKey = 'g' + g.n;
			if (prog[gKey]) {
				totalStars += prog[gKey].stars || 0;
				if ((prog[gKey].lv || 1) > 1) gamesPlayed++;
				maxLevel = Math.max(maxLevel, prog[gKey].lv || 1);
			}
		}
		return { totalStars, gamesPlayed, maxLevel };
	}
</script>

{#if !authenticated}
<div class="screen" style="display:flex">
	<h2>🔒 Zona de Padres</h2>
	{#if $parentPin}
		<p style="margin:10px 0">Introduce tu PIN de 4 dígitos:</p>
		<div style="display:flex;gap:8px;justify-content:center;margin:12px 0">
			<input type="password" maxlength="4" inputmode="numeric" pattern="[0-9]*" bind:value={pinInput}
				style="font-size:1.8rem;width:120px;text-align:center;border:3px solid var(--c5);border-radius:12px;padding:8px"
				onkeydown={(e) => e.key === 'Enter' && checkPin()} />
			<button class="btn" onclick={checkPin}>Entrar</button>
		</div>
		{#if pinError}<p style="color:#E53E3E">{pinError}</p>{/if}
	{:else}
		<p style="margin:16px 0">No tienes PIN configurado.</p>
		<button class="btn" onclick={() => { authenticated = true; }}>Entrar sin PIN</button>
	{/if}
	<button class="btn" style="margin-top:16px;background:var(--c5)" onclick={() => goto('/exploradores')}>← Volver</button>
</div>
{:else}
<div class="screen" style="display:flex">
	<h2>👨‍👩‍👧 Zona de Padres</h2>

	<div style="display:flex;gap:6px;flex-wrap:wrap;justify-content:center;margin:12px 0">
		<button class="btn" class:on={activeTab==='stats'} onclick={() => activeTab='stats'}>📊 Estadísticas</button>
		<button class="btn" class:on={activeTab==='settings'} onclick={() => activeTab='settings'}>⚙️ Ajustes</button>
		<button class="btn" class:on={activeTab==='support'} onclick={() => activeTab='support'}>☕ Apoyar</button>
	</div>

	{#if activeTab === 'stats'}
	<div style="width:100%;max-width:400px">
		<h3>Progreso por perfil</h3>
		{#each $profiles as prof, i}
			{@const stats = getProfileProgress(i)}
			<div style="background:var(--card);border-radius:12px;padding:12px;margin:8px 0;display:flex;align-items:center;gap:12px">
				<span style="font-size:2rem">{prof.avatar}</span>
				<div style="flex:1">
					<strong>{prof.name}</strong>
					<p style="font-size:.85rem;opacity:.7">⭐ {stats.totalStars} estrellas · 🎮 {stats.gamesPlayed} juegos · Nivel máx: {stats.maxLevel}</p>
				</div>
			</div>
		{/each}
		{#if $profiles.length === 0}
			<p style="opacity:.6;text-align:center">No hay perfiles creados aún.</p>
		{/if}
	</div>
	{:else if activeTab === 'settings'}
	<div style="width:100%;max-width:400px">
		<h3>Ajustes</h3>
		<label style="display:flex;align-items:center;gap:10px;margin:12px 0;font-size:1.1rem">
			<input type="checkbox" bind:checked={$night} style="width:22px;height:22px" /> 🌙 Modo noche
		</label>
		<label style="display:flex;align-items:center;gap:10px;margin:12px 0;font-size:1.1rem">
			<input type="checkbox" bind:checked={$muted} style="width:22px;height:22px" /> 🔇 Silenciar sonidos
		</label>
		<hr style="margin:16px 0;opacity:.2" />
		<h4>🔒 PIN parental</h4>
		{#if $parentPin}
			<p>PIN activo: ****</p>
			<div style="display:flex;gap:8px;margin:8px 0">
				<button class="btn" onclick={() => showSetPin=true}>Cambiar PIN</button>
				<button class="btn" style="background:#E53E3E" onclick={removePin}>Quitar PIN</button>
			</div>
		{:else}
			<p>Sin PIN configurado.</p>
			<button class="btn" onclick={() => showSetPin=true}>Configurar PIN</button>
		{/if}
		{#if showSetPin}
			<div style="display:flex;gap:8px;align-items:center;margin:10px 0">
				<input type="password" maxlength="4" inputmode="numeric" pattern="[0-9]*" bind:value={newPin}
					placeholder="4 dígitos" style="font-size:1.4rem;width:100px;text-align:center;border:2px solid var(--c5);border-radius:10px;padding:6px" />
				<button class="btn" onclick={savePin}>Guardar</button>
				<button class="btn" style="background:#999" onclick={() => { showSetPin=false; newPin=''; }}>Cancelar</button>
			</div>
		{/if}
	</div>
	{:else if activeTab === 'support'}
	<div style="width:100%;max-width:400px;text-align:center">
		<h3>☕ Apoya PinguPlay</h3>
		<p style="margin:12px 0;line-height:1.6">PinguPlay es gratis y sin anuncios. Si te gusta, puedes invitarme a un café para seguir mejorándolo.</p>
		<a href="https://ko-fi.com/pinguplay" target="_blank" rel="noopener noreferrer"
			style="display:inline-block;background:#FF5E5B;color:white;padding:12px 28px;border-radius:14px;font-size:1.2rem;font-weight:bold;text-decoration:none;margin:12px 0">
			☕ Invítame un café en Ko-Fi
		</a>
		<p style="font-size:.85rem;opacity:.5;margin-top:16px">PinguPlay v4 — Hecho con ❤️ para los más pequeños</p>
	</div>
	{/if}

	<button class="btn" style="margin-top:20px;background:var(--c5)" onclick={() => goto('/exploradores')}>← Volver al menú</button>
</div>
{/if}
