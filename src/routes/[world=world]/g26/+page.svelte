<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam } from '$lib/data.js';

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG26(cont, lv) {
		let round = 0;
		const total = lerpParam(lv, 6, 10);
		const maxNum = lerpParam(lv, 10, 100);

		cont.innerHTML = `<div class="ins">¿Mayor, menor o igual?</div>
			<div class="pbar"><div class="pfill" id="g26pb" style="width:0%;background:var(--c4)"></div></div>
			<div class="g26-comp" id="g26comp"></div>
			<div class="g26-btns" id="g26btns"></div>`;

		function next() {
			if (round >= total) { const _lv = window.ppWin(); window.ppCelebrate('¡Compara números genial! ⚖️', 3, () => initG26(cont, window.ppGetLevel()), _lv); return; }
			/** @type {HTMLElement} */ (cont.querySelector('#g26pb')).style.width = (round/total*100)+'%';
			let a = Math.floor(Math.random() * maxNum) + 1;
			let b;
			const r = Math.random();
			if (r < 0.15) b = a; // equal ~15%
			else b = Math.floor(Math.random() * maxNum) + 1;

			const compEl = /** @type {HTMLElement} */ (cont.querySelector('#g26comp'));
			compEl.innerHTML = `<span class="g26-n">${a}</span><span class="g26-q">?</span><span class="g26-n">${b}</span>`;

			const ans = a > b ? '>' : a < b ? '<' : '=';
			const labels = ['>','<','='];
			const btns = /** @type {HTMLElement} */ (cont.querySelector('#g26btns')); btns.innerHTML = '';
			labels.forEach(sym => {
				const btn = document.createElement('div');
				btn.className = 'g26-sym';
				btn.textContent = sym;
				btn.onclick = () => {
					if (sym === ans) {
						btn.style.background='#EFFFEF'; btn.style.borderColor='#6BCB77';
						/** @type {HTMLElement} */ (compEl.querySelector('.g26-q')).textContent = ans;
						window.ppBeep(880,.2);
						const word = ans==='>'?'mayor que':ans==='<'?'menor que':'igual a';
						window.ppSay(a + ' es ' + word + ' ' + b);
						window.ppOnCorrect(); round++;
						setTimeout(next, 1200);
					} else {
						btn.classList.add('err'); setTimeout(()=>btn.classList.remove('err'),400);
						window.ppOnWrong(); window.ppBoo(); window.ppSay('¡Inténtalo!');
					}
				};
				btns.appendChild(btn);
			});
			window.ppSay(a + ' y ' + b + '. ¿Mayor, menor o igual?');
		}
		next();
	}
</script>

<GameShell gameNum={26} title="Mayor/Menor" icon="⚖️" initGame={initG26} />
