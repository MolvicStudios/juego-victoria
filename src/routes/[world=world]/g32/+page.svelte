<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	/** @type {(key: string, vars?: Record<string, string|number>) => string} */ const T = (key, vars) => window.ppT?.(key, vars) ?? key;

	const G32_DATA = [
		{cats:['fruits','animals'],items:[{t:'🍎',c:0},{t:'🍊',c:0},{t:'🍇',c:0},{t:'🐶',c:1},{t:'🐱',c:1},{t:'🐰',c:1}]},
		{cats:['clothing','food'],items:[{t:'👕',c:0},{t:'👖',c:0},{t:'🧥',c:0},{t:'🍕',c:1},{t:'🌮',c:1},{t:'🍔',c:1}]},
		{cats:['land','water'],items:[{t:'🐕',c:0},{t:'🦁',c:0},{t:'🐘',c:0},{t:'🐟',c:1},{t:'🐙',c:1},{t:'🐋',c:1}]},
		{cats:['hot','cold'],items:[{t:'☀️',c:0},{t:'🔥',c:0},{t:'🌋',c:0},{t:'❄️',c:1},{t:'🧊',c:1},{t:'⛄',c:1}]},
		{cats:['flying','ground'],items:[{t:'✈️',c:0},{t:'🚁',c:0},{t:'🎈',c:0},{t:'🚗',c:1},{t:'🚌',c:1},{t:'🚂',c:1}]},
		{cats:['big','small'],items:[{t:'🐘',c:0},{t:'🦒',c:0},{t:'🐋',c:0},{t:'🐁',c:1},{t:'🐜',c:1},{t:'🐞',c:1}]},
		{cats:['fruits','vegetables'],items:[{t:'🍎',c:0},{t:'🍌',c:0},{t:'🍓',c:0},{t:'🥦',c:1},{t:'🥕',c:1},{t:'🌽',c:1}]},
		{cats:['daytime','nighttime'],items:[{t:'☀️',c:0},{t:'🌈',c:0},{t:'🦋',c:0},{t:'🌙',c:1},{t:'⭐',c:1},{t:'🦉',c:1}]},
	];

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG32(cont, lv) {
		let round = 0;
		const data = shuf(G32_DATA).slice(0, lerpParam(lv, 3, 6));

		cont.innerHTML = `<div class="ins">${T('games.g32.instruction')}</div>
			<div class="pbar"><div class="pfill" id="g32pb" style="width:0%;background:var(--c4)"></div></div>
			<div class="g32-cats" id="g32cats"></div>
			<div class="g32-items" id="g32items"></div>`;

		function next() {
			if (round >= data.length) { const _lv = window.ppWin(); window.ppCelebrate(T('games.g32.win') + ' 📂', 3, () => initG32(cont, window.ppGetLevel()), _lv); return; }
			/** @type {HTMLElement} */ (cont.querySelector('#g32pb')).style.width = (round/data.length*100)+'%';
			const d = data[round];
			const numPerCat = lerpParam(lv, 2, 3);
			const items0 = shuf(d.items.filter(i=>i.c===0)).slice(0, numPerCat);
			const items1 = shuf(d.items.filter(i=>i.c===1)).slice(0, numPerCat);
			const allItems = shuf([...items0, ...items1]);
			let sorted = 0;
			const totalItems = allItems.length;

			const catsEl = /** @type {HTMLElement} */ (cont.querySelector('#g32cats'));
			catsEl.innerHTML = '';
			const zones = d.cats.map((name, idx) => {
				const z = document.createElement('div');
				z.className = 'g32-zone';
				z.innerHTML = `<div class="g32-label">${T('games.g32.cats.'+name)}</div><div class="g32-drop" data-cat="${idx}"></div>`;
				catsEl.appendChild(z);
				return z;
			});

			const itemsEl = /** @type {HTMLElement} */ (cont.querySelector('#g32items'));
			itemsEl.innerHTML = '';
			/** @type {HTMLElement|null} */
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
				const drop = /** @type {HTMLElement} */ (z.querySelector('.g32-drop'));
				drop.onclick = () => {
					const sel = selected;
					if (!sel || sel.dataset.done) return;
					const item = allItems.find(i => i.t === sel.textContent);
					if (item && item.c === idx) {
						sel.style.outline = '';
						sel.style.background = '#EFFFEF';
						sel.style.border = '2px solid #6BCB77';
						sel.dataset.done = '1';
						drop.textContent += item.t;
						window.ppBeep(880,.1);
						window.ppOnCorrect();
						sorted++;
						selected = null;
						if (sorted >= totalItems) { round++; setTimeout(next, 800); }
					} else {
						sel.classList.add('err');
						setTimeout(()=>sel.classList.remove('err'),400);
						window.ppOnWrong(); window.ppBoo();
						sel.style.outline = '';
						selected = null;
					}
				};
			});
			window.ppSay(T('games.g32.prompt', {cats: d.cats.map(c => T('games.g32.cats.'+c)).join(T('games.g32.and'))}));
		}
		next();
	}
</script>

<GameShell gameNum={32} title="Categorías" icon="📂" initGame={initG32} />
