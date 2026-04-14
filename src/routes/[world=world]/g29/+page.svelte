<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	const T = (key, vars) => window.ppT?.(key, vars) ?? key;

	const G29_DATA=[
		{catKey:'fruits',items:['🍎','🍊','🍇','🍓'],intruder:'🚗'},
		{catKey:'animals',items:['🐶','🐱','🐰','🐸'],intruder:'🌮'},
		{catKey:'transport',items:['🚗','🚌','✈️','🚂'],intruder:'🍕'},
		{catKey:'clothing',items:['👕','👖','🧥','👗'],intruder:'🐟'},
		{catKey:'instruments',items:['🎸','🥁','🎹','🎺'],intruder:'🌻'},
		{catKey:'food',items:['🍕','🌮','🍔','🌭'],intruder:'📚'},
		{catKey:'flowers',items:['🌸','🌻','🌹','🌷'],intruder:'⚽'},
		{catKey:'sports',items:['⚽','🏀','🎾','🏐'],intruder:'🎸'},
		{catKey:'insects',items:['🐛','🦋','🐝','🐞'],intruder:'🎩'},
		{catKey:'weather',items:['☀️','🌧️','❄️','⛈️'],intruder:'🍌'},
		{catKey:'tools',items:['🔨','🔧','🪛','🪚'],intruder:'🦄'},
		{catKey:'trees',items:['🌲','🌳','🌴','🎄'],intruder:'🔑'},
	];

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG29(cont, lv) {
		let round = 0;
		const data = shuf(G29_DATA).slice(0, lerpParam(lv, 4, 8));

		cont.innerHTML = `<div class="ins">${T('games.g29.instruction')}</div>
			<div class="pbar"><div class="pfill" id="g29pb" style="width:0%;background:var(--c1)"></div></div>
			<div class="g29-hint" id="g29hint"></div>
			<div class="g29-grid" id="g29grid"></div>`;

		function next() {
			if (round >= data.length) { const _lv = window.ppWin(); window.ppCelebrate(T('games.g29.win'), 3, () => initG29(cont, window.ppGetLevel()), _lv); return; }
			/** @type {HTMLElement} */ (cont.querySelector('#g29pb')).style.width = (round/data.length*100)+'%';
			const d = data[round];
			const numItems = lerpParam(lv, 3, 4);
			const group = d.items.slice(0, numItems);
			const all = shuf([...group, d.intruder]);

			/** @type {HTMLElement} */ (cont.querySelector('#g29hint')).textContent = lv <= 5 ? T('games.g29.hint_group', {cat: T('games.g29.cats.' + d.catKey)}) : T('games.g29.hint_no_belong');

			const grid = /** @type {HTMLElement} */ (cont.querySelector('#g29grid')); grid.innerHTML = '';
			all.forEach(item => {
				const b = document.createElement('div');
				b.className = 'g29-item';
				b.textContent = item;
				b.onclick = () => {
					if (item === d.intruder) { b.style.background='#EFFFEF'; b.style.border='3px solid #6BCB77'; window.ppBeep(880,.2); window.ppSay(T('games.g29.correct', {cat: T('games.g29.cats.' + d.catKey)})); window.ppOnCorrect(); round++; setTimeout(next,1000); }
					else { b.classList.add('err'); setTimeout(()=>b.classList.remove('err'),400); window.ppOnWrong(); window.ppBoo(); }
				};
				grid.appendChild(b);
			});
			window.ppSay(T('games.g29.hello'));
		}
		next();
	}
</script>

<GameShell gameNum={29} title="El Intruso" icon="🔍" initGame={initG29} />
