<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	const T = (key, vars) => window.ppT?.(key, vars) ?? key;

	const COINS=[{v:1,lbl:'1c',col:'#cd7f32'},{v:2,lbl:'2c',col:'#cd7f32'},{v:5,lbl:'5c',col:'#cd7f32'},{v:10,lbl:'10c',col:'#C0C0C0'},{v:20,lbl:'20c',col:'#C0C0C0'},{v:50,lbl:'50c',col:'#FFD700'}];

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG27(cont, lv) {
		let round = 0;
		const total = lerpParam(lv, 5, 8);
		const maxTarget = lerpParam(lv, 10, 80);
		const maxCoins = lerpParam(lv, 3, 5);

		cont.innerHTML = `<div class="ins">${T('games.g27.instruction')}</div>
			<div class="pbar"><div class="pfill" id="g27pb" style="width:0%;background:var(--c5)"></div></div>
			<div class="g27-target" id="g27tgt"></div>
			<div class="g27-coins" id="g27coins"></div>
			<div class="g8-opts" id="g27opts"></div>`;

		function next() {
			if (round >= total) { const _lv = window.ppWin(); window.ppCelebrate(T('games.g27.win'), 3, () => initG27(cont, window.ppGetLevel()), _lv); return; }
			/** @type {HTMLElement} */ (cont.querySelector('#g27pb')).style.width = (round/total*100)+'%';

			// Generate coins that add up to a target
			const available = COINS.filter(c => c.v <= maxTarget);
			let sum = 0; const picked = [];
			for (let i = 0; i < maxCoins; i++) {
				const valid = available.filter(c => sum + c.v <= maxTarget);
				if (!valid.length) break;
				const c = valid[Math.floor(Math.random()*valid.length)];
				picked.push(c); sum += c.v;
			}
			if (sum === 0) { picked.push(available[0]); sum = available[0].v; }

			/** @type {HTMLElement} */ (cont.querySelector('#g27tgt')).textContent = T('games.g27.target');

			const coinsEl = /** @type {HTMLElement} */ (cont.querySelector('#g27coins')); coinsEl.innerHTML = '';
			shuf(picked).forEach(c => {
				const d = document.createElement('div');
				d.className = 'g27-coin';
				d.style.background = c.col;
				d.textContent = c.lbl;
				coinsEl.appendChild(d);
			});

			const numOpts = lv <= 3 ? 2 : lv <= 7 ? 3 : 4;
			const wrongs = new Set();
			let guard = 0;
			while (wrongs.size < numOpts - 1 && guard < 100) {
				guard++;
				const delta = Math.floor(Math.random() * 15) + 1;
				let w = Math.random() < 0.5 ? sum + delta : sum - delta;
				if (w < 1) w = sum + delta;
				if (w !== sum && !wrongs.has(w)) wrongs.add(w);
			}

			const optsEl = /** @type {HTMLElement} */ (cont.querySelector('#g27opts')); optsEl.innerHTML = '';
			const cols = ['#FF6B6B','#4D9FEC','#6BCB77','#FF9F43'];
			shuf([sum, ...wrongs]).forEach((v, i) => {
				const b = document.createElement('div');
				b.className = 'g2-num';
				b.style.background = cols[i % 4];
				b.textContent = v + 'c';
				b.onclick = () => {
					if (v === sum) { b.style.background='#EFFFEF'; b.style.borderColor='#6BCB77'; window.ppBeep(880,.2); window.ppSay(T('games.g27.correct', {sum})); window.ppOnCorrect(); round++; setTimeout(next, 1200); }
					else { b.classList.add('err'); setTimeout(()=>b.classList.remove('err'),400); window.ppOnWrong(); window.ppBoo(); window.ppSay(T('games.common.try_again')); }
				};
				optsEl.appendChild(b);
			});
			window.ppSay(T('games.g27.hello'));
		}
		next();
	}
</script>

<GameShell gameNum={27} title="Monedas" icon="🪙" initGame={initG27} />
