<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { onDestroy } from 'svelte';
	import { shuf, lerpParam } from '$lib/data.js';

	/** @type {(key: string, vars?: Record<string, string|number>) => string} */ const T = (key, vars) => window.ppT?.(key, vars) ?? key;

	/* 20 animals in increasing complexity: easy (top) → hard (bottom) */
	const ANIMALS = [
		{ e:'🐶', n:'dog' },      { e:'🐱', n:'cat' },      { e:'🐰', n:'rabbit' },
		{ e:'🐻', n:'bear' },     { e:'🐮', n:'cow' },      { e:'🐸', n:'frog' },
		{ e:'🐷', n:'pig' },      { e:'🦁', n:'lion' },     { e:'🐼', n:'panda' },
		{ e:'🦊', n:'fox' },      { e:'🐨', n:'koala' },    { e:'🐘', n:'elephant' },
		{ e:'🦒', n:'giraffe' },  { e:'🦓', n:'zebra' },    { e:'🐢', n:'turtle' },
		{ e:'🐺', n:'wolf' },     { e:'🦋', n:'butterfly' },{ e:'🐠', n:'fish' },
		{ e:'🦅', n:'eagle' },    { e:'🦄', n:'unicorn' },
	];

	/** @type {HTMLDivElement} */
	let container;
	let g18Round = 0;
	/** @type {{e:string,n:string}[]} */
	let g18Data = [];
	/** @type {ReturnType<typeof setTimeout>} */
	let g18HideTimer = /** @type {any} */ (0);
	onDestroy(() => clearTimeout(g18HideTimer));

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG18(cont, lv) {
		container = cont;
		g18Round = 0;
		/* Higher levels unlock more animals from the pool */
		const poolSize = Math.min(lerpParam(lv, 4, ANIMALS.length), ANIMALS.length);
		const total    = lerpParam(lv, 5, 12);
		g18Data = shuf(ANIMALS.slice(0, poolSize)).slice(0, total);

		container.innerHTML = `
			<div class="pbar"><div class="pfill" id="g18pb" style="width:0%;background:#FF9F43"></div></div>
			<div class="ins">${T('games.g18.instruction')}</div>
			<div class="g18-animal" id="g18em"></div>
			<div class="g3-opts" id="g18opts"></div>`;

		g18Show();
		window.ppSay(T('games.g18.hello'));
	}

	function g18Show() {
		if (!container) return;
		const lv = window.ppGetLevel();
		if (g18Round >= g18Data.length) {
			const _lv = window.ppWin();
			window.ppCelebrate(T('games.g18.win')+' 🐾', 3, () => initG18(container, window.ppGetLevel()), _lv);
			return;
		}
		const pb = /** @type {HTMLElement|null} */ (container.querySelector('#g18pb'));
		if (pb) pb.style.width = (g18Round / g18Data.length * 100) + '%';

		const animal = g18Data[g18Round];
		const emEl = /** @type {HTMLElement|null} */ (container.querySelector('#g18em'));
		if (emEl) { emEl.style.opacity = '1'; emEl.textContent = animal.e; }

		/* More distractor options at higher levels */
		const numOpts = lv <= 3 ? 2 : lv <= 8 ? 3 : 4;
		const distractors = shuf(ANIMALS.filter(a => a.n !== animal.n)).slice(0, numOpts - 1);
		const opts = shuf([animal, ...distractors]);

		const optsEl = container.querySelector('#g18opts');
		if (!optsEl) return;
		optsEl.innerHTML = '';

		opts.forEach(opt => {
			const b = document.createElement('div');
			b.className = 'g3-opt';
			/* Show emoji hint only up to level 9 */
			b.innerHTML = (lv <= 9 ? opt.e : '') + '<p>' + T('games.g18.animals.'+opt.n) + '</p>';
			b.onclick = () => {
				if (opt.n === animal.n) {
					b.style.background = '#EFFFEF'; b.style.borderColor = '#6BCB77';
					window.ppBeep(880, .2); window.ppOnCorrect();
					window.ppSay(T('games.g18.correct',{name:T('games.g18.animals.'+animal.n)}));
					g18Round++;
					setTimeout(g18Show, 1100);
				} else {
					b.classList.add('err');
					setTimeout(() => b.classList.remove('err'), 400);
					window.ppOnWrong(); window.ppBoo();
					window.ppSay(T('games.common.try_again'));
				}
			};
			optsEl.appendChild(b);
		});

		/* At level ≥ 12: hide the animal emoji after a moment (memory challenge) */
		if (lv >= 12) {
			clearTimeout(g18HideTimer);
			g18HideTimer = setTimeout(() => {
				const el = /** @type {HTMLElement|null} */ (container?.querySelector('#g18em'));
				if (el) el.style.opacity = '0';
			}, 1800);
		}

		window.ppSay(T('games.g18.instruction'));
	}

	/** @param {HTMLDivElement} c @param {number} lv */
	function initContainer(c, lv) { initG18(c, lv); }
</script>

<GameShell gameNum={18} title="Animales" icon="🐾" initGame={initContainer} />
