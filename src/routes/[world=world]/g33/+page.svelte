<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	/** @type {(key: string, vars?: Record<string, string|number>) => string} */ const T = (key, vars) => window.ppT?.(key, vars) ?? key;

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG33(cont, lv) {
		const size = lv <= 5 ? 3 : 4;
		const symbols = lv <= 5 ? ['🍎','🍊','🍇'] : ['🍎','🍊','🍇','🍋'];

		cont.innerHTML = `<div class="ins">${T('games.g33.instruction')}</div>
			<div class="g33-grid" id="g33grid" style="--sz:${size}"></div>
			<div class="g33-palette" id="g33pal"></div>`;

		// generate a valid solved grid
		/** @param {number} n */
		function genGrid(n) {
			const grid = Array.from({length:n}, ()=>Array(n).fill(0));
			/** @param {number} r @param {number} c */
			function fill(r,c) {
				if (r===n) return true;
				const nr = c===n-1?r+1:r;
				const nc = c===n-1?0:c+1;
				const vals = shuf(Array.from({length:n},(_,i)=>i+1));
				for (const v of vals) {
					if (grid[r].includes(v)) continue;
					if (grid.some(row=>row[c]===v)) continue;
					grid[r][c] = v;
					if (fill(nr, nc)) return true;
					grid[r][c] = 0;
				}
				return false;
			}
			fill(0,0);
			return grid;
		}

		const solution = genGrid(size);
		const puzzle = solution.map(r=>[...r]);
		// remove cells
		const blanks = [];
		const numBlanks = lerpParam(lv, 2, size===3?5:8);
		const positions = shuf(Array.from({length:size*size},(_,i)=>i)).slice(0, numBlanks);
		positions.forEach(p => {
			const r = Math.floor(p/size), c = p%size;
			puzzle[r][c] = 0;
			blanks.push({r,c,v:solution[r][c]});
		});

		/** @type {HTMLElement|null} */
		let selected = null;
		let filled = 0;

		const gridEl = /** @type {HTMLElement} */ (cont.querySelector('#g33grid'));
		gridEl.style.gridTemplateColumns = `repeat(${size}, 1fr)`;
		/** @type {HTMLDivElement[][]} */
		const cells = [];
		for (let r=0;r<size;r++) {
			cells[r]=[];
			for (let c=0;c<size;c++) {
				const cell = document.createElement('div');
				cell.className = 'g33-cell';
				if (puzzle[r][c]) {
					cell.textContent = symbols[puzzle[r][c]-1];
					cell.classList.add('g33-fixed');
				} else {
					cell.classList.add('g33-empty');
					cell.onclick = () => {
						if (cell.classList.contains('g33-fixed')) return;
						if (selected) selected.style.outline = '';
						selected = cell;
						cell.style.outline = '3px solid var(--c4)';
						cell.dataset.r = String(r); cell.dataset.c = String(c);
					};
				}
				cells[r][c] = cell;
				gridEl.appendChild(cell);
			}
		}

		const palEl = /** @type {HTMLElement} */ (cont.querySelector('#g33pal'));
		symbols.forEach((sym, i) => {
			const b = document.createElement('div');
			b.className = 'g33-sym';
			b.textContent = sym;
			b.onclick = () => {
				const sel = selected;
				if (!sel || sel.classList.contains('g33-fixed')) return;
				const r = +(sel.dataset.r||'0'), c = +(sel.dataset.c||'0');
				const val = i + 1;
				if (solution[r][c] === val) {
					sel.textContent = sym;
					sel.classList.remove('g33-empty');
					sel.classList.add('g33-fixed');
					sel.style.outline = '';
					sel.style.background = '#EFFFEF';
					window.ppBeep(880,.1);
					window.ppOnCorrect();
					selected = null;
					filled++;
					if (filled >= blanks.length) {
						const _lv = window.ppWin();
						window.ppCelebrate(T('games.g33.win') + ' 🧩', 3, () => initG33(cont, window.ppGetLevel()), _lv);
					}
				} else {
					sel.classList.add('err');
					setTimeout(()=>sel.classList.remove('err'),400);
					window.ppOnWrong(); window.ppBoo();
				}
			};
			palEl.appendChild(b);
		});
		window.ppSay(T('games.g33.hello'));
	}
</script>

<GameShell gameNum={33} title="Sudoku Mini" icon="🧩" initGame={initG33} />
