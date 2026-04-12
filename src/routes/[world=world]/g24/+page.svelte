<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	const FRUITS=['🍎','🍊','🍋','🍇','🍓','🍌','🫐','🍑','🥝','🍒'];

	function initG24(cont, lv) {
		let round = 0;
		const total = lerpParam(lv, 5, 8);

		cont.innerHTML = `<div class="ins">¡Resta las frutas!</div>
			<div class="pbar"><div class="pfill" id="g24pb" style="width:0%;background:var(--c2)"></div></div>
			<div class="g24-visual" id="g24vis"></div>
			<div class="g24-eq" id="g24eq"></div>
			<div class="g8-opts" id="g24opts"></div>`;

		function next() {
			if (round >= total) { const _lv = window.ppWin(); window.ppCelebrate('¡Restando como un campeón! ➖', 3, () => initG24(cont, window.ppGetLevel()), _lv); return; }
			cont.querySelector('#g24pb').style.width = (round/total*100)+'%';
			const maxA = lerpParam(lv, 5, 15);
			const a = Math.floor(Math.random() * (maxA - 1)) + 2;
			const b = Math.floor(Math.random() * a) + 1;
			const ans = a - b;
			const fruit = FRUITS[Math.floor(Math.random() * FRUITS.length)];

			const vis = cont.querySelector('#g24vis');
			vis.innerHTML = '';
			for (let i = 0; i < a; i++) {
				const sp = document.createElement('span');
				sp.className = 'g24-fruit';
				sp.textContent = fruit;
				if (i >= a - b) sp.classList.add('g24-crossed');
				vis.appendChild(sp);
			}

			cont.querySelector('#g24eq').textContent = `${a} − ${b} = ?`;

			const numOpts = lv <= 3 ? 2 : lv <= 7 ? 3 : 4;
			const wrongs = new Set();
			while (wrongs.size < numOpts - 1) {
				let w = ans + (Math.random() < 0.5 ? 1 : -1) * (Math.floor(Math.random() * 3) + 1);
				if (w < 0) w = ans + Math.floor(Math.random() * 3) + 1;
				if (w !== ans && w >= 0) wrongs.add(w);
			}

			const optsEl = cont.querySelector('#g24opts'); optsEl.innerHTML = '';
			shuf([ans, ...wrongs]).forEach(c => {
				const btn = document.createElement('div');
				btn.className = 'g2-num';
				btn.textContent = c;
				btn.onclick = () => {
					if (c === ans) { btn.style.background='#EFFFEF'; btn.style.borderColor='#6BCB77'; window.ppBeep(880,.2); window.ppSay('¡Correcto! ' + a + ' menos ' + b + ' es ' + ans); window.ppOnCorrect(); round++; setTimeout(next, 1200); }
					else { btn.classList.add('err'); setTimeout(()=>btn.classList.remove('err'),400); window.ppOnWrong(); window.ppBoo(); }
				};
				optsEl.appendChild(btn);
			});
			window.ppSay(a + ' menos ' + b);
		}
		next();
	}
</script>

<GameShell gameNum={24} title="Restas" icon="➖" initGame={initG24} />
