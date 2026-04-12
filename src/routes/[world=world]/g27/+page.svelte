<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	const COINS=[{v:1,lbl:'1c',col:'#cd7f32'},{v:2,lbl:'2c',col:'#cd7f32'},{v:5,lbl:'5c',col:'#cd7f32'},{v:10,lbl:'10c',col:'#C0C0C0'},{v:20,lbl:'20c',col:'#C0C0C0'},{v:50,lbl:'50c',col:'#FFD700'}];

	function initG27(cont, lv) {
		let round = 0;
		const total = lerpParam(lv, 5, 8);
		const maxTarget = lerpParam(lv, 10, 80);
		const maxCoins = lerpParam(lv, 3, 5);

		cont.innerHTML = `<div class="ins">¡Cuenta las monedas!</div>
			<div class="pbar"><div class="pfill" id="g27pb" style="width:0%;background:var(--c5)"></div></div>
			<div class="g27-target" id="g27tgt"></div>
			<div class="g27-coins" id="g27coins"></div>
			<div class="g8-opts" id="g27opts"></div>`;

		function next() {
			if (round >= total) { const _lv = window.ppWin(); window.ppCelebrate('¡Cuentas monedas genial! 🪙', 3, () => initG27(cont, window.ppGetLevel()), _lv); return; }
			cont.querySelector('#g27pb').style.width = (round/total*100)+'%';

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

			cont.querySelector('#g27tgt').textContent = '¿Cuánto suman?';

			const coinsEl = cont.querySelector('#g27coins'); coinsEl.innerHTML = '';
			shuf(picked).forEach(c => {
				const d = document.createElement('div');
				d.className = 'g27-coin';
				d.style.background = c.col;
				d.textContent = c.lbl;
				coinsEl.appendChild(d);
			});

			const numOpts = lv <= 3 ? 2 : lv <= 7 ? 3 : 4;
			const wrongs = new Set();
			while (wrongs.size < numOpts - 1) {
				let w = sum + (Math.random() < 0.5 ? 1 : -1) * (Math.floor(Math.random() * 15) + 1);
				if (w < 1) w = sum + Math.floor(Math.random() * 10) + 1;
				if (w !== sum) wrongs.add(w);
			}

			const optsEl = cont.querySelector('#g27opts'); optsEl.innerHTML = '';
			shuf([sum, ...wrongs]).forEach(v => {
				const b = document.createElement('div');
				b.className = 'g2-num';
				b.textContent = v + 'c';
				b.onclick = () => {
					if (v === sum) { b.style.background='#EFFFEF'; b.style.borderColor='#6BCB77'; window.ppBeep(880,.2); window.ppSay('¡Correcto! Suman ' + sum); window.ppOnCorrect(); round++; setTimeout(next, 1200); }
					else { b.classList.add('err'); setTimeout(()=>b.classList.remove('err'),400); window.ppOnWrong(); window.ppBoo(); window.ppSay('¡Inténtalo!'); }
				};
				optsEl.appendChild(b);
			});
			window.ppSay('¿Cuánto suman las monedas?');
		}
		next();
	}
</script>

<GameShell gameNum={27} title="Monedas" icon="🪙" initGame={initG27} />
