<script>
	import { locale, LOCALES, t } from '$lib/i18n/index.js';

	/**
	 * @prop {'onboarding'|'settings'} variant
	 * @prop {(()=>void)=} onConfirm  — called after confirm in onboarding variant
	 */
	let { variant = 'onboarding', onConfirm } = $props();

	const LOCALE_KEYS = /** @type {(keyof typeof LOCALES)[]} */ (Object.keys(LOCALES));

	let selected = $state(/** @type {string} */ ($locale));
	// Sync if external locale changes
	locale.subscribe(v => { selected = v; });

	function choose(code) {
		selected = code;
		if (variant === 'settings') {
			locale.set(code);
		}
	}

	function confirm() {
		locale.set(selected);
		if (onConfirm) onConfirm();
	}

	// Reactive confirm button text: updates as user selects different language
	function confirmLabel() {
		return LOCALES[selected]?.confirmBtn ?? '¡Vamos!';
	}
</script>

{#if variant === 'onboarding'}
	<!-- ─── Onboarding selector: 2+2+1 centered grid ─── -->
	<div class="lsel-onboard" role="radiogroup" aria-labelledby="lsel-title">
		<h2 class="lsel-title" id="lsel-title">{$t('ui.lang.select_title')}</h2>
		<div class="lsel-grid">
			{#each LOCALE_KEYS as code}
				<!-- svelte-ignore a11y_no_static_element_interactions -->
				<div
					class="lsel-card {selected === code ? 'sel' : ''}"
					role="radio"
					aria-checked={selected === code}
					tabindex="0"
					onclick={() => choose(code)}
					onkeydown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); choose(code); } }}
				>
					<span class="lsel-flag" aria-hidden="true">{@html FLAGS[code]}</span>
					<span class="lsel-name">{LOCALES[code].nativeName}</span>
				</div>
			{/each}
		</div>
		<button class="lsel-confirm" onclick={confirm}>{confirmLabel()}</button>
	</div>

{:else}
	<!-- ─── Settings variant: vertical list with instant select ─── -->
	<div class="lsel-settings" role="radiogroup" aria-label={$t('ui.settings.language')}>
		{#each LOCALE_KEYS as code}
			<!-- svelte-ignore a11y_no_static_element_interactions -->
			<div
				class="lsel-row {selected === code ? 'sel' : ''}"
				role="radio"
				aria-checked={selected === code}
				tabindex="0"
				onclick={() => choose(code)}
				onkeydown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); choose(code); } }}
			>
				<span class="lsel-flag-sm" aria-hidden="true">{@html FLAGS[code]}</span>
				<span class="lsel-row-name">{LOCALES[code].nativeName}</span>
				{#if selected === code}
					<span class="lsel-check" aria-hidden="true">✓</span>
				{/if}
			</div>
		{/each}
	</div>
{/if}

<script module>
	/** Inline SVG flags — no external assets needed */
	export const FLAGS = {
		es: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 40" width="48" height="32" aria-hidden="true">
			<rect width="60" height="40" fill="#AA151B"/>
			<rect y="10" width="60" height="20" fill="#F1BF00"/>
		</svg>`,
		en: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 40" width="48" height="32" aria-hidden="true">
			<rect width="60" height="40" fill="#012169"/>
			<path d="M0,0 L60,40 M60,0 L0,40" stroke="#fff" stroke-width="6"/>
			<path d="M0,0 L60,40 M60,0 L0,40" stroke="#C8102E" stroke-width="4"/>
			<path d="M30,0 V40 M0,20 H60" stroke="#fff" stroke-width="10"/>
			<path d="M30,0 V40 M0,20 H60" stroke="#C8102E" stroke-width="6"/>
		</svg>`,
		ca: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 40" width="48" height="32" aria-hidden="true">
			<rect width="60" height="40" fill="#FCDD09"/>
			<rect y="5" width="60" height="5" fill="#DA121A"/>
			<rect y="15" width="60" height="5" fill="#DA121A"/>
			<rect y="25" width="60" height="5" fill="#DA121A"/>
			<rect y="35" width="60" height="5" fill="#DA121A"/>
		</svg>`,
		eu: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 40" width="48" height="32" aria-hidden="true">
			<rect width="60" height="40" fill="#fff"/>
			<path d="M30,0 V40 M0,20 H60" stroke="#D7281F" stroke-width="10"/>
			<path d="M0,0 L60,40 M60,0 L0,40" stroke="#2B7F3B" stroke-width="6"/>
		</svg>`,
		gl: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 40" width="48" height="32" aria-hidden="true">
			<rect width="60" height="40" fill="#fff"/>
			<rect y="24" width="60" height="16" fill="#009AC7"/>
			<path d="M0,0 V40 M5,0 V40" stroke="#009AC7" stroke-width="3"/>
			<path d="M60,0 V40 M55,0 V40" stroke="#009AC7" stroke-width="3"/>
		</svg>`,
	};
</script>

<style>
	/* ── Onboarding ── */
	.lsel-onboard {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 18px;
		padding: 24px 16px;
	}
	.lsel-title {
		font-size: 1.25rem;
		font-weight: 800;
		color: var(--ink, #1a1a2e);
		margin: 0;
		text-align: center;
	}
	.lsel-grid {
		display: grid;
		grid-template-columns: repeat(2, 90px);
		gap: 12px;
		justify-content: center;
	}
	/* 5th item (gl) centered */
	.lsel-grid > :nth-child(5) {
		grid-column: 1 / 3;
		justify-self: center;
	}
	.lsel-card {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		width: 90px;
		height: 80px;
		border-radius: 16px;
		border: 3px solid transparent;
		background: #fff;
		cursor: pointer;
		gap: 6px;
		box-shadow: 0 2px 8px rgba(0,0,0,.10);
		transition: transform .12s, border-color .12s, box-shadow .12s;
		user-select: none;
	}
	.lsel-card:hover { transform: translateY(-2px); box-shadow: 0 4px 14px rgba(0,0,0,.14); }
	.lsel-card.sel {
		border-color: var(--c4, #6BCB77);
		box-shadow: 0 0 0 4px color-mix(in srgb, var(--c4,#6BCB77) 25%, transparent);
	}
	.lsel-card:focus-visible { outline: 3px solid var(--c4, #6BCB77); outline-offset: 2px; }
	.lsel-flag { display: flex; line-height: 1; }
	.lsel-flag :global(svg) { width: 48px; height: 32px; border-radius: 3px; }
	.lsel-name { font-size: .8rem; font-weight: 700; color: var(--ink, #1a1a2e); }
	.lsel-confirm {
		margin-top: 4px;
		padding: 12px 36px;
		border-radius: 24px;
		background: var(--c4, #6BCB77);
		color: #fff;
		font-size: 1.1rem;
		font-weight: 800;
		border: none;
		cursor: pointer;
		box-shadow: 0 4px 12px rgba(107,203,119,.35);
		transition: transform .1s, filter .1s;
	}
	.lsel-confirm:hover { filter: brightness(1.08); }
	.lsel-confirm:active { transform: scale(.96); }

	/* ── Settings ── */
	.lsel-settings {
		display: flex;
		flex-direction: column;
		gap: 4px;
	}
	.lsel-row {
		display: flex;
		align-items: center;
		gap: 10px;
		padding: 8px 10px;
		border-radius: 10px;
		cursor: pointer;
		transition: background .1s;
	}
	.lsel-row:hover { background: rgba(107,203,119,.12); }
	.lsel-row.sel { background: rgba(107,203,119,.20); }
	.lsel-row:focus-visible { outline: 2px solid var(--c4, #6BCB77); }
	.lsel-flag-sm { display: flex; }
	.lsel-flag-sm :global(svg) { width: 24px; height: 16px; border-radius: 2px; }
	.lsel-row-name { font-size: .9rem; font-weight: 600; color: var(--ink, #1a1a2e); flex: 1; }
	.lsel-check { font-size: .9rem; color: var(--c4, #6BCB77); font-weight: 800; }
</style>
