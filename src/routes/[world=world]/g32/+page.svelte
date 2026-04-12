<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	const G32_DATA = [
		{cats:['Frutas 🍎','Animales 🐾'],items:[{t:'🍎',c:0},{t:'🍊',c:0},{t:'🍇',c:0},{t:'🐶',c:1},{t:'🐱',c:1},{t:'🐰',c:1}]},
		{cats:['Ropa 👕','Comida 🍔'],items:[{t:'👕',c:0},{t:'👖',c:0},{t:'🧥',c:0},{t:'🍕',c:1},{t:'🌮',c:1},{t:'🍔',c:1}]},
		{cats:['Tierra 🌍','Agua 🌊'],items:[{t:'🐕',c:0},{t:'🦁',c:0},{t:'🐘',c:0},{t:'🐟',c:1},{t:'🐙',c:1},{t:'🐋',c:1}]},
		{cats:['Caliente 🔥','Frío ❄️'],items:[{t:'☀️',c:0},{t:'🔥',c:0},{t:'🌋',c:0},{t:'❄️',c:1},{t:'🧊',c:1},{t:'⛄',c:1}]},
		{cats:['Voladores ✈️','Terrestres 🚗'],items:[{t:'✈️',c:0},{t:'🚁',c:0},{t:'🎈',c:0},{t:'🚗',c:1},{t:'🚌',c:1},{t:'🚂',c:1}]},
		{cats:['Grande 🐘','Pequeño 🐁'],items:[{t:'🐘',c:0},{t:'🦒',c:0},{t:'🐋',c:0},{t:'🐁',c:1},{t:'🐜',c:1},{t:'🐞',c:1}]},
		{cats:['Frutas 🍎','Verduras 🥦'],items:[{t:'🍎',c:0},{t:'🍌',c:0},{t:'🍓',c:0},{t:'🥦',c:1},{t:'🥕',c:1},{t:'🌽',c:1}]},
		{cats:['Día ☀️','Noche 🌙'],items:[{t:'☀️',c:0},{t:'🌈',c:0},{t:'🦋',c:0},{t:'🌙',c:1},{t:'⭐',c:1},{t:'🦉',c:1}]},
	];

	function initG32(cont, lv) {
		let round = 0;
		const data = shuf(G32_DATA).slice(0, lerpParam(lv, 3, 6));

		cont.innerHTML = `<div class="ins">¡Clasifica en categorías!</div>
			<div class="pbar"><div class="pfill" id="g32pb" style="width:0%;background:var(--c4)"></div></div>
			<div class="g32-cats" id="g32cats"></div>
			<div class="g32-items" id="g32items"></div>`;

		function next() {
			if (round >= data.length) { const _lv = window.ppWin(); window.ppCelebrate('¡Clasificas genial! 📂', 3, () => initG32(cont, window.ppGetLevel()), _lv); return; }
			cont.querySelector('#g32pb').style.width = (round/data.length*100)+'%';
			const d = data[round];
			const numPerCat = lerpParam(lv, 2, 3);
			const items0 = shuf(d.items.filter(i=>i.c===0)).slice(0, numPerCat);
			const items1 = shuf(d.items.filter(i=>i.c===1)).slice(0, numPerCat);
			const allItems = shuf([...items0, ...items1]);
			let sorted = 0;
			const totalItems = allItems.length;

			const catsEl = cont.querySelector('#g32cats');
			catsEl.innerHTML = '';
			const zones = d.cats.map((name, idx) => {
				const z = document.createElement('div');
				z.className = 'g32-zone';
				z.innerHTML = `<div class="g32-label">${name}</div><div class="g32-drop" data-cat="${idx}"></div>`;
				catsEl.appendChild(z);
				return z;
			});

			const itemsEl = cont.querySelector('#g32items');
			itemsEl.innerHTML = '';
			let selected = null;
			allItems.forEach(item => {
				const el = document.createElement('div');
				el.className = 'g29-item';
				el.textContent = item.t;
				el.onclick = () => {
					if (el.dataset.done) return;
					if (selected) selected.style.outline='';
					selected = el;
					el.style.outline = '3px solid var(--c4)';
				};
				itemsEl.appendChild(el);
			});

			zones.forEach((z, idx) => {
				const drop = z.querySelector('.g32-drop');
				drop.onclick = () => {
					if (!selected || selected.dataset.done) return;
					const item = allItems.find(i => i.t === selected.textContent);
					if (item && item.c === idx) {
						selected.style.outline = '';
						selected.style.background = '#EFFFEF';
						selected.style.border = '2px solid #6BCB77';
						selected.dataset.done = '1';
						drop.textContent += item.t;
						window.ppBeep(880,.1);
						window.ppOnCorrect();
						sorted++;
						selected = null;
						if (sorted >= totalItems) { round++; setTimeout(next, 800); }
					} else {
						selected.classList.add('err');
						setTimeout(()=>selected.classList.remove('err'),400);
						window.ppOnWrong(); window.ppBoo();
						selected.style.outline = '';
						selected = null;
					}
				};
			});
			window.ppSay('Clasifica los elementos en: ' + d.cats.join(' y '));
		}
		next();
	}
</script>

<GameShell gameNum={32} title="Categorías" icon="📂" initGame={initG32} />
