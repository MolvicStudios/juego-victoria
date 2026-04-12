<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { profiles, activeProfileIndex, worldForAge } from '$lib/stores/profiles.js';
	import { allProgress } from '$lib/stores/progress.js';
	import { parentPin, night, muted } from '$lib/stores/settings.js';
	import { GAMES } from '$lib/data.js';
	import { get } from 'svelte/store';

	let authenticated = $state(false);
	let pinInput = $state('');
	let pinError = $state('');
	let activeTab = $state('stats');
	let showSetPin = $state(false);
	let newPin = $state('');
	let profileList = $state([]);
	let progressData = $state({});
	let storedPin = $state('');

	profiles.subscribe(v => { profileList = v; });
	allProgress.subscribe(v => { progressData = v; });
	parentPin.subscribe(v => { storedPin = v; });

	onMount(() => {
		if (!storedPin) authenticated = true;
	});

	function checkPin() {
		if (pinInput === storedPin) { authenticated = true; pinError = ''; }
		else { pinError = 'PIN incorrecto'; pinInput = ''; }
	}

	function savePin() {
		if (newPin.length === 4 && /^\d{4}$/.test(newPin)) {
			parentPin.set(newPin);
			showSetPin = false; newPin = '';
		}
	}

	function removePin() { parentPin.set(''); }

	function getProfileStats(idx) {
		const key = 'p' + idx;
		const prog = progressData[key] || {};
		const stars = prog.stars || 0;
		const levels = prog.levels || {};
		const maxLevels = prog.maxLevels || {};
		let gamesPlayed = 0, highestLevel = 0;
		for (const g of GAMES) {
			const lv = levels[g.n] || 1;
			const ml = maxLevels[g.n] || 1;
			if (ml > 1) gamesPlayed++;
			if (ml > highestLevel) highestLevel = ml;
		}
		return { stars, gamesPlayed, highestLevel, totalGames: GAMES.length };
	}

	function goBack() {
		const idx = get(activeProfileIndex);
		const profs = get(profiles);
		if (idx >= 0 && idx < profs.length) goto('/' + worldForAge(profs[idx].birthYear));
		else goto('/');
	}

	const WORLD_INFO = {
		nubecitas:    { emoji: '☁️', label: 'Nubecitas', age: '0-2' },
		exploradores: { emoji: '🌏', label: 'Exploradores', age: '3-5' },
		aventureros:  { emoji: '⚔️', label: 'Aventureros', age: '6-8' },
		maestros:     { emoji: '🏆', label: 'Maestros', age: '9-12' },
	};
</script>

<style>
	.pad-wrap{flex:1;display:flex;flex-direction:column;align-items:center;padding:16px 16px 80px;
		overflow-y:auto;z-index:10;min-height:100%;gap:14px}
	.pad-header{text-align:center}
	.pad-header h1{font-size:1.3rem;margin-bottom:4px}
	.pad-header p{font-size:.82rem;color:var(--ink2)}
	.pad-tabs{display:flex;gap:6px;flex-wrap:wrap;justify-content:center}
	.pad-tab{padding:10px 16px;border-radius:14px;border:2px solid #EEE;background:var(--card);
		font-size:.82rem;font-weight:700;cursor:pointer;font-family:'Nunito',sans-serif;color:var(--ink);transition:all .15s}
	.pad-tab.on{background:var(--c6);color:#fff;border-color:var(--c6)}
	.pad-section{width:100%;max-width:480px;background:var(--card-glass);backdrop-filter:blur(14px);
		-webkit-backdrop-filter:blur(14px);border:var(--glass-border);border-radius:18px;
		padding:20px;box-shadow:var(--shadow)}
	.pad-section h3{font-size:1rem;margin-bottom:10px}
	.pad-section h4{font-size:.88rem;margin:14px 0 8px;font-weight:900}
	.pad-section p{font-size:.85rem;line-height:1.6;color:var(--ink2);margin:6px 0}
	.stat-card{display:flex;align-items:center;gap:12px;padding:12px;border-radius:14px;
		background:rgba(0,0,0,.03);margin:8px 0}
	.stat-av{font-size:2rem;width:48px;height:48px;display:flex;align-items:center;justify-content:center;
		border-radius:14px;background:var(--card);box-shadow:var(--shadow)}
	.stat-info{flex:1}.stat-info strong{font-size:.95rem}
	.stat-info small{display:block;font-size:.78rem;color:var(--ink2);margin-top:2px}
	.stat-bar{height:8px;border-radius:6px;background:#EEE;overflow:hidden;margin-top:6px}
	.stat-fill{height:100%;border-radius:6px;transition:width .4s}
	.pin-row{display:flex;gap:8px;align-items:center;margin:10px 0;flex-wrap:wrap}
	.pin-inp{font-size:1.4rem;width:100px;text-align:center;border:2px solid var(--c5);
		border-radius:12px;padding:8px;font-family:'Nunito',sans-serif;background:var(--card);color:var(--ink)}
	.pad-btn{padding:10px 20px;border-radius:14px;border:none;font-size:.85rem;font-weight:700;
		cursor:pointer;font-family:'Nunito',sans-serif;color:#fff;transition:transform .12s}
	.pad-btn:active{transform:scale(.94)}
	.pad-btn-pri{background:var(--c6)}
	.pad-btn-red{background:#E53E3E}
	.pad-btn-gray{background:#999}
	.pad-btn-back{background:var(--c5);margin-top:8px}
	.info-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:12px 0}
	.info-card{text-align:center;padding:14px 8px;border-radius:14px;background:rgba(0,0,0,.03)}
	.info-card .ig-emoji{font-size:1.8rem;display:block;margin-bottom:4px}
	.info-card .ig-label{font-size:.72rem;font-weight:700;color:var(--ink)}
	.info-card .ig-val{font-size:.65rem;color:var(--ink2)}
	.toggle-row{display:flex;align-items:center;gap:12px;padding:10px 0}
	.toggle-row span{font-size:1rem}
	.toggle-row label{flex:1;font-size:.9rem;font-weight:700}
	.toggle-sw{appearance:none;-webkit-appearance:none;width:48px;height:28px;border-radius:20px;
		background:#CCC;position:relative;cursor:pointer;transition:background .2s;flex-shrink:0}
	.toggle-sw:checked{background:var(--c4)}
	.toggle-sw::before{content:'';position:absolute;top:3px;left:3px;width:22px;height:22px;
		border-radius:50%;background:#fff;transition:transform .2s;box-shadow:0 2px 4px rgba(0,0,0,.15)}
	.toggle-sw:checked::before{transform:translateX(20px)}
	.world-table{width:100%;border-collapse:separate;border-spacing:0 6px;font-size:.78rem}
	.world-table td{padding:8px;background:rgba(0,0,0,.02);vertical-align:middle}
	.world-table td:first-child{border-radius:10px 0 0 10px;font-weight:700;white-space:nowrap}
	.world-table td:last-child{border-radius:0 10px 10px 0}
</style>

{#if !authenticated}
<div class="scr on" style="display:flex">
	<div class="pad-wrap">
		<div class="pad-header">
			<h1>🔒 Zona de Padres</h1>
			<p>Introduce tu PIN para acceder</p>
		</div>

		<div class="pad-section" style="text-align:center">
			<p style="margin-bottom:12px">PIN de 4 dígitos:</p>
			<div class="pin-row" style="justify-content:center">
				<input type="password" maxlength="4" inputmode="numeric" pattern="[0-9]*"
					bind:value={pinInput} class="pin-inp"
					onkeydown={(e) => e.key === 'Enter' && checkPin()} />
				<button class="pad-btn pad-btn-pri" onclick={checkPin}>Entrar</button>
			</div>
			{#if pinError}<p style="color:#E53E3E;font-weight:700;margin-top:8px">{pinError}</p>{/if}
		</div>

		<button class="pad-btn pad-btn-back" onclick={() => goto('/')}>← Volver al inicio</button>
	</div>
</div>

{:else}
<div class="scr on" style="display:flex">
	<div class="pad-wrap">
		<div class="pad-header">
			<h1>👨‍👩‍👧 Zona de Padres</h1>
			<p>Controla el progreso y configura la app</p>
		</div>

		<div class="pad-tabs">
			<button class="pad-tab {activeTab === 'stats' ? 'on' : ''}" onclick={() => activeTab='stats'}>📊 Progreso</button>
			<button class="pad-tab {activeTab === 'info' ? 'on' : ''}" onclick={() => activeTab='info'}>📚 Contenido</button>
			<button class="pad-tab {activeTab === 'settings' ? 'on' : ''}" onclick={() => activeTab='settings'}>⚙️ Ajustes</button>
			<button class="pad-tab {activeTab === 'about' ? 'on' : ''}" onclick={() => activeTab='about'}>ℹ️ Acerca de</button>
		</div>

		<!-- ═══════ ESTADÍSTICAS ═══════ -->
		{#if activeTab === 'stats'}
		<div class="pad-section">
			<h3>📊 Progreso de los perfiles</h3>
			{#each profileList as prof, i}
				{@const stats = getProfileStats(i)}
				{@const world = worldForAge(prof.birthYear)}
				{@const wInfo = WORLD_INFO[world]}
				<div class="stat-card">
					<div class="stat-av">{prof.avatar}</div>
					<div class="stat-info">
						<strong>{prof.name}</strong>
						<small>{wInfo.emoji} {wInfo.label} ({wInfo.age} años)</small>
						<small>⭐ {stats.stars} estrellas · 🎮 {stats.gamesPlayed}/{stats.totalGames} juegos · 🏅 Nivel máx: {stats.highestLevel}</small>
						<div class="stat-bar">
							<div class="stat-fill" style="width:{Math.round(stats.gamesPlayed / stats.totalGames * 100)}%;background:var(--c4)"></div>
						</div>
					</div>
				</div>
			{/each}
			{#if profileList.length === 0}
				<p style="text-align:center;opacity:.6;padding:20px 0">No hay perfiles creados aún. Vuelve al inicio para crear uno.</p>
			{/if}
		</div>

		<!-- ═══════ CONTENIDO EDUCATIVO ═══════ -->
		{:else if activeTab === 'info'}
		<div class="pad-section">
			<h3>📚 ¿Qué aprenden?</h3>
			<p>PinguPlay tiene <strong>18 juegos educativos</strong> con <strong>15 niveles</strong> de dificultad cada uno. La dificultad sube automáticamente cuando tu hijo avanza:</p>

			<h4>🧠 Áreas de aprendizaje</h4>
			<div class="info-grid">
				<div class="info-card"><span class="ig-emoji">🔷</span><span class="ig-label">Lógica espacial</span><span class="ig-val">Formas, Puzles, Patrones</span></div>
				<div class="info-card"><span class="ig-emoji">🔢</span><span class="ig-label">Matemáticas</span><span class="ig-val">Contar, Sumas, Números</span></div>
				<div class="info-card"><span class="ig-emoji">🅰️</span><span class="ig-label">Lectoescritura</span><span class="ig-val">Letras, Traza, ¿Qué ves?</span></div>
				<div class="info-card"><span class="ig-emoji">🎨</span><span class="ig-label">Creatividad</span><span class="ig-val">Pintar, Piano, Colores</span></div>
				<div class="info-card"><span class="ig-emoji">🧩</span><span class="ig-label">Memoria</span><span class="ig-val">Parejas, Sonidos, Animales</span></div>
				<div class="info-card"><span class="ig-emoji">📏</span><span class="ig-label">Comparación</span><span class="ig-val">Grande/Pequeño, Patrones</span></div>
			</div>

			<h4>🌍 4 mundos adaptados por edad</h4>
			<table class="world-table">
				<tbody>
				<tr><td>☁️ Nubecitas</td><td>0-2 años: juegos táctiles y visuales con estímulos simples</td></tr>
				<tr><td>🌏 Exploradores</td><td>3-5 años: letras, números, colores y formas básicas</td></tr>
				<tr><td>⚔️ Aventureros</td><td>6-8 años: laberintos, sumas, trazado y lógica</td></tr>
				<tr><td>🏆 Maestros</td><td>9-12 años: desafíos avanzados con patrones y aritmética</td></tr>
				</tbody>
			</table>

			<h4>⬆️ Sistema de dificultad adaptativa</h4>
			<p>Cada juego tiene 15 niveles. Al completar un nivel, se desbloquea el siguiente. Si tu hijo falla 3 veces seguidas, el juego baja un nivel automáticamente para evitar frustración.</p>
			<p>Las ⭐ estrellas ganadas desbloquean stickers coleccionables (hay 20 logros de 5⭐ a 2000⭐).</p>
		</div>

		<!-- ═══════ AJUSTES ═══════ -->
		{:else if activeTab === 'settings'}
		<div class="pad-section">
			<h3>⚙️ Ajustes</h3>

			<div class="toggle-row">
				<span>🌙</span>
				<label>Modo noche</label>
				<input type="checkbox" class="toggle-sw" bind:checked={$night} />
			</div>

			<div class="toggle-row">
				<span>🔇</span>
				<label>Silenciar sonidos y voz</label>
				<input type="checkbox" class="toggle-sw" bind:checked={$muted} />
			</div>

			<hr style="margin:16px 0;opacity:.15" />

			<h4>🔒 PIN parental</h4>
			<p>El PIN protege esta zona para que solo los adultos puedan acceder a los ajustes y estadísticas.</p>

			{#if storedPin}
				<p style="font-weight:700">PIN activo: ••••</p>
				<div class="pin-row">
					<button class="pad-btn pad-btn-pri" onclick={() => showSetPin = true}>Cambiar PIN</button>
					<button class="pad-btn pad-btn-red" onclick={removePin}>Quitar PIN</button>
				</div>
			{:else}
				<p>Sin PIN configurado. Cualquiera puede acceder a esta zona.</p>
				<button class="pad-btn pad-btn-pri" onclick={() => showSetPin = true}>Configurar PIN</button>
			{/if}

			{#if showSetPin}
				<div class="pin-row" style="margin-top:12px">
					<input type="password" maxlength="4" inputmode="numeric" pattern="[0-9]*"
						bind:value={newPin} class="pin-inp" placeholder="4 dígitos" />
					<button class="pad-btn pad-btn-pri" onclick={savePin}>Guardar</button>
					<button class="pad-btn pad-btn-gray" onclick={() => { showSetPin = false; newPin = ''; }}>Cancelar</button>
				</div>
			{/if}

			<hr style="margin:16px 0;opacity:.15" />

			<h4>🗑️ Gestión de datos</h4>
			<p>Todos los datos se guardan localmente en este dispositivo. No se envía nada a ningún servidor.</p>
		</div>

		<!-- ═══════ ACERCA DE ═══════ -->
		{:else if activeTab === 'about'}
		<div class="pad-section">
			<h3>ℹ️ Acerca de PinguPlay</h3>
			<p style="text-align:center;font-size:3rem;margin:8px 0">🐧</p>
			<p style="text-align:center;font-weight:900;font-size:1.1rem">PinguPlay v5</p>
			<p style="text-align:center;font-size:.78rem;color:var(--ink2)">18 juegos · 15 niveles · 4 mundos</p>

			<h4>🔒 Privacidad y seguridad</h4>
			<p>PinguPlay fue diseñado pensando en la seguridad de los niños:</p>
			<p>✅ <strong>Sin publicidad</strong> — Ningún anuncio dentro de la app</p>
			<p>✅ <strong>Sin rastreo</strong> — No se recopilan datos de uso ni analíticas</p>
			<p>✅ <strong>100% offline</strong> — Funciona sin conexión a internet</p>
			<p>✅ <strong>Datos locales</strong> — Todo se guarda solo en el dispositivo</p>
			<p>✅ <strong>Sin compras</strong> — Todo el contenido es gratuito</p>
			<p>✅ <strong>Sin enlaces externos</strong> — Los niños no pueden salir de la app</p>

			<h4>☕ Apoya el proyecto</h4>
			<p>PinguPlay es gratis y sin anuncios. Si te gusta, puedes ayudar a mantenerlo:</p>
			<a href="https://ko-fi.com/pinguplay" target="_blank" rel="noopener noreferrer"
				style="display:block;text-align:center;background:#FF5E5B;color:white;padding:14px 28px;
				border-radius:14px;font-size:1rem;font-weight:bold;text-decoration:none;margin:12px 0;
				box-shadow:0 4px 0 rgba(200,60,60,.3)">
				☕ Invítame un café en Ko-Fi
			</a>

			<h4>📧 Contacto</h4>
			<p>¿Sugerencias o problemas? Escríbenos:</p>
			<p style="font-weight:700;text-align:center">hola@molvicstudios.com</p>

			<div style="margin-top:16px;text-align:center;font-size:.7rem;color:var(--ink2)">
				<p>© 2026 MolvicStudios · Hecho con ❤️ para los más pequeños</p>
				<p style="margin-top:6px"><a href="/privacy.html" style="color:var(--ink2)">Privacidad</a> · <a href="/terms.html" style="color:var(--ink2)">Términos</a></p>
			</div>
		</div>
		{/if}

		<button class="pad-btn pad-btn-back" onclick={goBack}>← Volver</button>
	</div>
</div>
{/if}
