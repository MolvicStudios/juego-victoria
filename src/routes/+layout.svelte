<script>
	import '../app.css';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { night, muted } from '$lib/stores/settings.js';
	import { toggleMute } from '$lib/audio.js';

	let { children } = $props();
	let mounted = $state(false);
	let pathname = $state('/');
	page.subscribe(p => { pathname = p.url.pathname; });
	const hideHome = $derived(pathname === '/' || pathname === '/padres');
	let isNight = $state(false);
	let isMuted = $state(false);

	night.subscribe(v => { isNight = v; });
	muted.subscribe(v => { isMuted = v; });

	onMount(() => {
		mounted = true;
		createScenery();
		applyNight(isNight);
	});

	function applyNight(n) {
		if (typeof document === 'undefined') return;
		document.documentElement.classList.toggle('night', n);
	}

	$effect(() => { if (mounted) applyNight(isNight); });

	function createScenery() {
		document.querySelectorAll('.cloud,.star').forEach(e => e.remove());
		for (let i = 0; i < 6; i++) {
			const cl = document.createElement('div'); cl.className = 'cloud';
			const s = 40 + Math.random() * 60;
			cl.style.cssText = `width:${s}px;height:${s*.5}px;top:${5+Math.random()*25}%;
				left:${Math.random()*80}%;box-shadow:${s*.3}px ${s*.1}px 0 0 #fff,${-s*.2}px ${s*.05}px 0 0 #fff;
				animation:drift ${40+Math.random()*40}s linear infinite;animation-delay:${-Math.random()*40}s`;
			document.body.appendChild(cl);
		}
		for (let i = 0; i < 30; i++) {
			const st = document.createElement('div'); st.className = 'star';
			const s = 2 + Math.random() * 3;
			st.style.cssText = `width:${s}px;height:${s}px;top:${5+Math.random()*40}%;left:${Math.random()*100}%;
				animation-delay:${Math.random()*3}s`;
			document.body.appendChild(st);
		}
	}
</script>

<div class="sky {isNight ? 'sky-night' : 'sky-day'}"></div>
<div class="hills {isNight ? 'hills-night' : 'hills-day'}"></div>

{@render children()}

{#if !hideHome}
<button id="home-btn" onclick={() => goto('/')} title="Inicio" aria-label="Volver al inicio">🏠</button>
{/if}
<button id="mute" onclick={toggleMute}>{isMuted ? '🔇' : '🔊'}</button>
