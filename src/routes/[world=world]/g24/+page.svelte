<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	const T = (key, vars) => window.ppT?.(key, vars) ?? key;

	const FRUITS=['🍎','🍊','🍋','🍇','🍓','🍌','🫐','🍑','🥝','🍒'];

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG24(cont, lv) {
		let round = 0;
		const total = lerpParam(lv, 5, 8);

		cont.innerHTML = `<div class="ins">${T('games.g24.instruction')}</div>
			<div class="pbar"><div class="pfill" id="g24pb" style="width:0%;background:var(--c2)"></div></div>
			<div class="g24-visual" id="g24vis"></div>
			<div class="g24-eq" id="g24eq"></div>
			<div class="g8-opts" id="g24opts"></div>`;

		function next() {
			if (round >= total) { const _lv = window.ppWin(); window.ppCelebrate(T('games.g24.win'), 3, () => initG24(cont, window.ppGetLevel()), _lv); return; }
			/** @type {HTMLElement} */ (cont.querySelector('#g24pb')).style.width = (round/total*100)+'%';
			const maxA = lerpParam(lv, 5, 15);
			const a = Math.floor(Math.random() * (maxA - 1)) + 2;
			const b = Math.floor(Math.random() * a) + 1;
			const ans = a - b;
			const fruit = FRUITS[Math.floor(Math.random() * FRUITS.length)];

			const vis = /** @type {HTMLElement} */ (cont.querySelector('#g24vis'));
			vis.innerHTML = '';
			for (let i = 0; i < a; i++) {
				const sp = document.createElement('span');
				sp.className = 'g24-fruit';
				sp.textContent = fruit;
				if (i >= a - b) sp.classList.add('g24-crossed');
				vis.appendChild(sp);
			}

			/** @type {HTMLElement} */ (cont.querySelector('#g24eq')).textContent = `${a} − ${b} = ?`;

			const numOpts = lv <= 3 ? 2 : lv <= 7 ? 3 : 4;
			const wrongs = new Set();
			while (wrongs.size < numOpts - 1) {
				let w = ans + (Math.random() < 0.5 ? 1 : -1) * (Math.floor(Math.random() * 3) + 1);
				if (w < 0) w = ans + Math.floor(Math.random() * 3) + 1;
				if (w !== ans && w >= 0) wrongs.add(w);
			}

			const optsEl = /** @type {HTMLElement} */ (cont.querySelector('#g24opts')); optsEl.innerHTML = '';
			const cols = ['#FF6B6B','#4D9FEC','#6BCB77','#FF9F43'];
			shuf([ans, ...wrongs]).forEach((c, i) => {
				const btn = document.createElement('div');
				btn.className = 'g2-num';
				btn.style.background = cols[i % 4];
				btn.textContent = String(c);
				btn.onclick = () => {
					if (c === ans) { btn.style.background='#EFFFEF'; btn.style.borderColor='#6BCB77'; window.ppBeep(880,.2); window.ppSay(T('games.g24.correct', {a, b, ans})); window.ppOnCorrect(); round++; setTimeout(next, 1200); }
					else { btn.classList.add('err'); setTimeout(()=>btn.classList.remove('err'),400); window.ppOnWrong(); window.ppBoo(); window.ppSay(T('games.common.try_again')); }
				};
				optsEl.appendChild(btn);
			});
			window.ppSay(T('games.g24.prompt', {a, b}));
		}
		next();
	}
</script>

<GameShell gameNum={24} title="Restas" icon="➖" initGame={initG24} />
