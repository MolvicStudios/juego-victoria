<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	const G29_DATA=[
		{cat:'Frutas',items:['🍎','🍊','🍇','🍓'],intruder:'🚗'},
		{cat:'Animales',items:['🐶','🐱','🐰','🐸'],intruder:'🌮'},
		{cat:'Transportes',items:['🚗','🚌','✈️','🚂'],intruder:'🍕'},
		{cat:'Ropa',items:['👕','👖','🧥','👗'],intruder:'🐟'},
		{cat:'Instrumentos',items:['🎸','🥁','🎹','🎺'],intruder:'🌻'},
		{cat:'Comida',items:['🍕','🌮','🍔','🌭'],intruder:'📚'},
		{cat:'Flores',items:['🌸','🌻','🌹','🌷'],intruder:'⚽'},
		{cat:'Deportes',items:['⚽','🏀','🎾','🏐'],intruder:'🎸'},
		{cat:'Insectos',items:['🐛','🦋','🐝','🐞'],intruder:'🎩'},
		{cat:'Clima',items:['☀️','🌧️','❄️','⛈️'],intruder:'🍌'},
		{cat:'Herramientas',items:['🔨','🔧','🪛','🪚'],intruder:'🦄'},
		{cat:'Árboles',items:['🌲','🌳','🌴','🎄'],intruder:'🔑'},
	];

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG29(cont, lv) {
		let round = 0;
		const data = shuf(G29_DATA).slice(0, lerpParam(lv, 4, 8));

		cont.innerHTML = `<div class="ins">¡Encuentra el intruso!</div>
			<div class="pbar"><div class="pfill" id="g29pb" style="width:0%;background:var(--c1)"></div></div>
			<div class="g29-hint" id="g29hint"></div>
			<div class="g29-grid" id="g29grid"></div>`;

		function next() {
			if (round >= data.length) { const _lv = window.ppWin(); window.ppCelebrate('¡Detective de intrusos! 🔍', 3, () => initG29(cont, window.ppGetLevel()), _lv); return; }
			/** @type {HTMLElement} */ (cont.querySelector('#g29pb')).style.width = (round/data.length*100)+'%';
			const d = data[round];
			const numItems = lerpParam(lv, 3, 4);
			const group = d.items.slice(0, numItems);
			const all = shuf([...group, d.intruder]);

			/** @type {HTMLElement} */ (cont.querySelector('#g29hint')).textContent = lv <= 5 ? 'Grupo: ' + d.cat : '¿Cuál no pertenece?';

			const grid = /** @type {HTMLElement} */ (cont.querySelector('#g29grid')); grid.innerHTML = '';
			all.forEach(item => {
				const b = document.createElement('div');
				b.className = 'g29-item';
				b.textContent = item;
				b.onclick = () => {
					if (item === d.intruder) { b.style.background='#EFFFEF'; b.style.border='3px solid #6BCB77'; window.ppBeep(880,.2); window.ppSay('¡Correcto! No es ' + d.cat); window.ppOnCorrect(); round++; setTimeout(next,1000); }
					else { b.classList.add('err'); setTimeout(()=>b.classList.remove('err'),400); window.ppOnWrong(); window.ppBoo(); }
				};
				grid.appendChild(b);
			});
			window.ppSay('¿Cuál es el intruso?');
		}
		next();
	}
</script>

<GameShell gameNum={29} title="El Intruso" icon="🔍" initGame={initG29} />
