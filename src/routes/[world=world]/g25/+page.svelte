<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	const T = (key, vars) => window.ppT?.(key, vars) ?? key;

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG25(cont, lv) {
		let round = 0;
		const total = lerpParam(lv, 6, 10);
		const maxNum = lerpParam(lv, 10, 50);

		cont.innerHTML = `<div class="ins">${T('games.g25.instruction')}</div>
			<div class="pbar"><div class="pfill" id="g25pb" style="width:0%;background:var(--c3)"></div></div>
			<div class="g25-num" id="g25n"></div>
			<div class="g25-btns" id="g25btns"></div>`;

		const used = new Set();
		function pickNum() {
			let n;
			let tries = 0;
			do { n = Math.floor(Math.random() * maxNum) + 1; tries++; } while (used.has(n) && tries < 50);
			used.add(n);
			return n;
		}

		function next() {
			if (round >= total) { const _lv = window.ppWin(); window.ppCelebrate(T('games.g25.win'), 3, () => initG25(cont, window.ppGetLevel()), _lv); return; }
			/** @type {HTMLElement} */ (cont.querySelector('#g25pb')).style.width = (round/total*100)+'%';
			const num = pickNum();
			const isPar = num % 2 === 0;
			/** @type {HTMLElement} */ (cont.querySelector('#g25n')).textContent = String(num);

			const btns = /** @type {HTMLElement} */ (cont.querySelector('#g25btns'));
			btns.innerHTML = '';
			['par','impar'].forEach((key, idx) => {
				const b = document.createElement('div');
				b.className = 'g25-btn';
				b.textContent = T('games.g25.'+key);
				b.onclick = () => {
					const correct = (idx === 0 && isPar) || (idx === 1 && !isPar);
					if (correct) { b.style.background='#EFFFEF'; b.style.borderColor='#6BCB77'; window.ppBeep(880,.2); window.ppSay(T('games.g25.correct', {n: num, type: T('games.g25.'+(isPar?'par_lower':'impar_lower'))})); window.ppOnCorrect(); round++; setTimeout(next, 1000); }
					else { b.classList.add('err'); setTimeout(()=>b.classList.remove('err'),400); window.ppOnWrong(); window.ppBoo(); window.ppSay(T('games.common.try_again')); }
				};
				btns.appendChild(b);
			});
			window.ppSay(T('games.g25.question', {n: num}));
		}
		next();
	}
</script>

<GameShell gameNum={25} title="Par o Impar" icon="🔢" initGame={initG25} />
