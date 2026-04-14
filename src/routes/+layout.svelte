<script>
	import '../app.css';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { night, muted, hiContrast, bigText } from '$lib/stores/settings.js';
	import { toggleMute } from '$lib/audio.js';
	import { initI18n, t, locale } from '$lib/i18n/index.js';

	let { children } = $props();
	let mounted = $state(false);
	let pathname = $state('/');
	page.subscribe(p => { pathname = p.url.pathname; });
	const hideHome = $derived(pathname === '/' || pathname === '/padres');
	let isNight = $state(false);
	let isMuted = $state(false);
	let isHiContrast = $state(false);
	let isBigText = $state(false);
	let soundPlaying = $state(false);
	/** @type {'pending'|'accepted'|'declined'} */
	let cookieConsent = $state('pending');

	night.subscribe(v => { isNight = v; });
	muted.subscribe(v => { isMuted = v; });
	hiContrast.subscribe(v => { isHiContrast = v; });
	bigText.subscribe(v => { isBigText = v; });

	onMount(() => {
		initI18n();
		locale.subscribe(loc => { document.documentElement.lang = loc; });
		mounted = true;
		createScenery();
		applyNight(isNight);
		const saved = localStorage.getItem('pp_cookie_consent');
		if (saved === 'accepted' || saved === 'declined') cookieConsent = /** @type {any} */ (saved);
		const onSound = () => { soundPlaying = true; setTimeout(() => { soundPlaying = false; }, 1200); };
		document.addEventListener('pp-sound', onSound);
		return () => { document.removeEventListener('pp-sound', onSound); };
	});

	$effect(() => {
		if (mounted) {
			document.documentElement.classList.toggle('hc', isHiContrast);
			document.documentElement.classList.toggle('big', isBigText);
		}
	});

	function acceptCookies() {
		localStorage.setItem('pp_cookie_consent', 'accepted');
		cookieConsent = 'accepted';
		if (typeof window !== 'undefined' && typeof (/** @type {any} */(window)).gtag === 'function') {
			(/** @type {any} */(window)).gtag('consent', 'update', { analytics_storage: 'granted' });
		}
	}

	function declineCookies() {
		localStorage.setItem('pp_cookie_consent', 'declined');
		cookieConsent = 'declined';
	}

	/** @param {boolean} n */
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
<div class="snd-ind {soundPlaying ? 'on' : ''}">🔊</div>

{#if cookieConsent === 'pending'}
<div class="cookie-banner" role="dialog" aria-label={$t('ui.cookie.text')}>
	<div class="cookie-text">
		<span>🍪</span>
		<p>{$t('ui.cookie.text')} <a href="/privacy.html" target="_blank">{$t('ui.cookie.more_info')}</a></p>
	</div>
	<div class="cookie-btns">
		<button class="cookie-accept" onclick={acceptCookies}>{$t('ui.cookie.accept')}</button>
		<button class="cookie-decline" onclick={declineCookies}>{$t('ui.cookie.decline')}</button>
	</div>
</div>
{/if}
