<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG36(cont, lv) {
		let round = 0;
		const total = lerpParam(lv, 4, 7);
		const gridSize = lv <= 4 ? 3 : lv <= 8 ? 4 : 5;
		const numFilled = lerpParam(lv, 2, Math.floor(gridSize*gridSize*0.6));
		const COLORS = ['#E74C3C','#3498DB','#2ECC71','#F39C12','#9B59B6','#1ABC9C'];

		cont.innerHTML = `<div class="ins">¡Copia el patrón!</div>
			<div class="pbar"><div class="pfill" id="g36pb" style="width:0%;background:var(--c6)"></div></div>
			<div class="g36-grids">
				<div class="g36-grid" id="g36model" style="--sz:${gridSize}"></div>
				<div class="g36-grid" id="g36player" style="--sz:${gridSize}"></div>
			</div>`;

		function next() {
			if (round >= total) { const _lv = window.ppWin(); window.ppCelebrate('¡Espejo perfecto! 🪞', 3, () => initG36(cont, window.ppGetLevel()), _lv); return; }
			/** @type {HTMLElement} */ (cont.querySelector('#g36pb')).style.width = (round/total*100)+'%';

			const pattern = Array(gridSize*gridSize).fill(null);
			const positions = shuf(Array.from({length:gridSize*gridSize},(_,i)=>i)).slice(0, numFilled);
			const useColor = lv >= 6;
			const col = useColor ? COLORS[Math.floor(Math.random()*COLORS.length)] : '#3498DB';
			positions.forEach(p => pattern[p] = col);

			let correct = 0;
			const targetCorrect = positions.length;

			// model grid
			const model = /** @type {HTMLElement} */ (cont.querySelector('#g36model')); model.innerHTML = '';
			model.style.gridTemplateColumns = `repeat(${gridSize},1fr)`;
			pattern.forEach(c => {
				const cell = document.createElement('div');
				cell.className = 'g36-cell';
				if (c) cell.style.background = c;
				model.appendChild(cell);
			});

			// player grid
			const player = /** @type {HTMLElement} */ (cont.querySelector('#g36player')); player.innerHTML = '';
			player.style.gridTemplateColumns = `repeat(${gridSize},1fr)`;
			pattern.forEach((c, i) => {
				const cell = document.createElement('div');
				cell.className = 'g36-cell g36-clickable';
				cell.onclick = () => {
					if (cell.dataset.done) return;
					if (c) {
						cell.style.background = c;
						cell.dataset.done = '1';
						correct++;
						window.ppBeep(600,.1);
						window.ppOnCorrect();
						if (correct >= targetCorrect) { round++; setTimeout(next, 800); }
					} else {
						cell.classList.add('err');
						setTimeout(()=>cell.classList.remove('err'), 400);
						window.ppOnWrong(); window.ppBoo();
					}
				};
				player.appendChild(cell);
			});
			window.ppSay('¡Copia el patrón en la cuadrícula vacía!');
		}
		next();
	}
</script>

<GameShell gameNum={36} title="Espejo" icon="🪞" initGame={initG36} />
