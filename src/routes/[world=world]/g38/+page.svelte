<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	function initG38(cont, lv) {
		let round = 0;
		const total = lerpParam(lv, 3, 6);
		const COLORS = ['#E74C3C','#3498DB','#2ECC71','#F1C40F','#9B59B6','#E67E22'];

		// Tangram-style: arrange pieces to match a target shape
		const PUZZLES = [
			{name:'Cuadrado', pieces:[{x:0,y:0,w:1,h:1},{x:1,y:0,w:1,h:1},{x:0,y:1,w:1,h:1},{x:1,y:1,w:1,h:1}]},
			{name:'Rectángulo',pieces:[{x:0,y:0,w:2,h:1},{x:0,y:1,w:1,h:1},{x:1,y:1,w:1,h:1}]},
			{name:'Forma L',pieces:[{x:0,y:0,w:1,h:1},{x:0,y:1,w:1,h:1},{x:0,y:2,w:1,h:1},{x:1,y:2,w:1,h:1}]},
			{name:'Forma T',pieces:[{x:0,y:0,w:1,h:1},{x:1,y:0,w:1,h:1},{x:2,y:0,w:1,h:1},{x:1,y:1,w:1,h:1}]},
			{name:'Cruz',pieces:[{x:1,y:0,w:1,h:1},{x:0,y:1,w:1,h:1},{x:1,y:1,w:1,h:1},{x:2,y:1,w:1,h:1},{x:1,y:2,w:1,h:1}]},
			{name:'Escalera',pieces:[{x:0,y:0,w:1,h:1},{x:0,y:1,w:1,h:1},{x:1,y:1,w:1,h:1},{x:1,y:2,w:1,h:1},{x:2,y:2,w:1,h:1}]},
		];

		const puzzlePool = shuf(PUZZLES).slice(0, total);

		cont.innerHTML = `<div class="ins">¡Coloca las piezas!</div>
			<div class="pbar"><div class="pfill" id="g38pb" style="width:0%;background:var(--c1)"></div></div>
			<div class="g38-name" id="g38name"></div>
			<div class="g38-board" id="g38board"></div>
			<div class="g38-pieces" id="g38pieces"></div>`;

		function next() {
			if (round >= total) { const _lv = window.ppWin(); window.ppCelebrate('¡Constructor maestro! 🏗️', 3, () => initG38(cont, window.ppGetLevel()), _lv); return; }
			cont.querySelector('#g38pb').style.width = (round/total*100)+'%';

			const puzzle = puzzlePool[round];
			cont.querySelector('#g38name').textContent = puzzle.name;

			// Compute grid bounds
			let maxX=0, maxY=0;
			puzzle.pieces.forEach(p=>{maxX=Math.max(maxX,p.x+p.w);maxY=Math.max(maxY,p.y+p.h);});

			const cellSize = Math.min(60, Math.floor(250/Math.max(maxX,maxY)));
			const board = cont.querySelector('#g38board');
			board.innerHTML = '';
			board.style.cssText = `display:grid;grid-template-columns:repeat(${maxX},${cellSize}px);grid-template-rows:repeat(${maxY},${cellSize}px);gap:2px;margin:8px auto;width:fit-content;`;

			// Create board cells
			const slots = [];
			for (let y=0;y<maxY;y++) {
				for (let x=0;x<maxX;x++) {
					const cell = document.createElement('div');
					cell.style.cssText = `width:${cellSize}px;height:${cellSize}px;border-radius:4px;`;
					const hasPiece = puzzle.pieces.some(p=>x>=p.x&&x<p.x+p.w&&y>=p.y&&y<p.y+p.h);
					if (hasPiece) {
						cell.className = 'g38-slot';
						cell.dataset.x = x; cell.dataset.y = y;
						slots.push(cell);
					} else {
						cell.style.background = 'transparent';
					}
					board.appendChild(cell);
				}
			}

			// Create draggable pieces
			let placed = 0;
			let selected = null;
			const piecesEl = cont.querySelector('#g38pieces'); piecesEl.innerHTML='';
			const shuffledPieces = shuf([...puzzle.pieces]);
			shuffledPieces.forEach((p, i) => {
				const piece = document.createElement('div');
				piece.className = 'g38-piece';
				piece.style.cssText = `width:${cellSize}px;height:${cellSize}px;background:${COLORS[i%COLORS.length]};border-radius:6px;display:inline-block;margin:4px;cursor:pointer;border:2px solid rgba(0,0,0,0.2);`;
				piece.dataset.idx = i;
				piece.textContent = (i+1);
				piece.style.fontSize = (cellSize*0.5)+'px';
				piece.style.color = '#fff';
				piece.style.fontWeight = '900';
				piece.style.textAlign = 'center';
				piece.style.lineHeight = cellSize+'px';
				piece.onclick = () => {
					if (piece.dataset.done) return;
					if (selected) selected.style.outline='';
					selected = piece;
					piece.style.outline = '3px solid #333';
				};
				piecesEl.appendChild(piece);
			});

			slots.forEach(slot => {
				slot.onclick = () => {
					if (!selected || selected.dataset.done) return;
					if (slot.dataset.filled) return;
					slot.style.background = selected.style.background;
					slot.dataset.filled = '1';
					selected.dataset.done = '1';
					selected.style.opacity = '0.3';
					selected.style.outline = '';
					window.ppBeep(600,.1);
					window.ppOnCorrect();
					placed++;
					selected = null;
					if (placed >= puzzle.pieces.length) {
						round++; setTimeout(next, 800);
					}
				};
			});
			window.ppSay('¡Coloca las piezas para formar: ' + puzzle.name + '!');
		}
		next();
	}
</script>

<GameShell gameNum={38} title="Tangram" icon="🏗️" initGame={initG38} />
