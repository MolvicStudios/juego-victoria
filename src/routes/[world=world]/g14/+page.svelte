<script>
	import { onMount, onDestroy } from 'svelte';
	import GameShell from '$lib/components/GameShell.svelte';
	import { shuf } from '$lib/data.js';

	const T = (key, vars) => window.ppT?.(key, vars) ?? key;

	/** @type {((e:KeyboardEvent)=>void)|undefined} */
	let keyHandler;

	/** @param {number} rows @param {number} cols */
	function generateMaze(rows,cols){
		const grid=Array.from({length:rows},()=>Array.from({length:cols},()=>({n:true,s:true,e:true,w:true,vis:false})));
		/** @param {number} r @param {number} c */
		function dfs(r,c){
			grid[r][c].vis=true;
			const dirs=shuf([{dr:-1,dc:0,wall:'n',opp:'s'},{dr:1,dc:0,wall:'s',opp:'n'},{dr:0,dc:-1,wall:'w',opp:'e'},{dr:0,dc:1,wall:'e',opp:'w'}]);
			for(const{dr,dc,wall,opp}of dirs){
				const nr=r+dr,nc=c+dc;
				if(nr>=0&&nr<rows&&nc>=0&&nc<cols&&!grid[nr][nc].vis){/** @type {any} */ (grid[r][c])[wall]=false;/** @type {any} */ (grid[nr][nc])[opp]=false;dfs(nr,nc);}
			}
		}
		dfs(0,0);return grid;
	}

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG14(cont, lv) {
		const rows=lv<=3?3:lv<=6?4:lv<=9?5:lv<=12?6:7;
		const cols=rows;
		let maze=generateMaze(rows,cols),pr=0,pc=0;

		function render(){
			const el=/** @type {HTMLElement} */ (cont.querySelector('#g14maze'));
			const cellSz=Math.min(Math.floor((Math.min(window.innerWidth,440)-24)/cols),70);
			el.style.gridTemplateColumns=`repeat(${cols},${cellSz}px)`;
			el.style.gridTemplateRows=`repeat(${rows},${cellSz}px)`;
			el.innerHTML='';
			const bw=3;
			for(let r=0;r<rows;r++){
				for(let c=0;c<cols;c++){
					const cell=document.createElement('div');cell.className='g14-cell';
					cell.dataset.r=String(r);cell.dataset.c=String(c);
					const m=maze[r][c];
					cell.style.borderTop=m.n?bw+'px solid var(--ink)':bw+'px solid transparent';
					cell.style.borderBottom=m.s?bw+'px solid var(--ink)':bw+'px solid transparent';
					cell.style.borderLeft=m.w?bw+'px solid var(--ink)':bw+'px solid transparent';
					cell.style.borderRight=m.e?bw+'px solid var(--ink)':bw+'px solid transparent';
					cell.style.width=cellSz+'px';cell.style.height=cellSz+'px';
					if(r===pr&&c===pc){cell.textContent='🐧';cell.classList.add('player');}
					if(r===rows-1&&c===cols-1){cell.textContent+='🐟';cell.classList.add('goal');}
					cell.onclick=()=>move(parseInt(cell.dataset.r||'0'),parseInt(cell.dataset.c||'0'));
					el.appendChild(cell);
				}
			}
		}

		/** @param {number} r @param {number} c */
		function move(r,c){
			const dr=r-pr,dc=c-pc;
			if(Math.abs(dr)+Math.abs(dc)!==1)return;
			const cur=maze[pr][pc];
			if(dr===-1&&cur.n)return;if(dr===1&&cur.s)return;
			if(dc===-1&&cur.w)return;if(dc===1&&cur.e)return;
			pr=r;pc=c;window.ppBeep(500,.08);render();
			if(r===rows-1&&c===cols-1){
				window.ppOnCorrect();const _lv=window.ppWin();
				setTimeout(()=>window.ppCelebrate(T('games.g14.win'),3,()=>initG14(cont,window.ppGetLevel()),_lv),300);
			}
		}

		/** @param {string} dir */
		function moveDir(dir){
			const m2={up:[-1,0],down:[1,0],left:[0,-1],right:[0,1]}[dir];
			if(m2)move(pr+m2[0],pc+m2[1]);
		}

		cont.innerHTML = `<div class="ins">${T('games.g14.instruction')}</div>
			<div class="g14-maze" id="g14maze"></div>
			<div class="dpad"><button class="dpad-btn" id="dp-u">▲</button>
			<div class="dp-mid"><button class="dpad-btn" id="dp-l">◀</button><button class="dpad-btn" id="dp-r">▶</button></div>
			<button class="dpad-btn" id="dp-d">▼</button></div>`;

		/** @type {HTMLElement} */ (cont.querySelector('#dp-u')).onclick=()=>moveDir('up');
		/** @type {HTMLElement} */ (cont.querySelector('#dp-d')).onclick=()=>moveDir('down');
		/** @type {HTMLElement} */ (cont.querySelector('#dp-l')).onclick=()=>moveDir('left');
		/** @type {HTMLElement} */ (cont.querySelector('#dp-r')).onclick=()=>moveDir('right');

		if(keyHandler) document.removeEventListener('keydown', keyHandler);
		keyHandler = e => {
			if(e.key==='ArrowUp')moveDir('up');
			else if(e.key==='ArrowDown')moveDir('down');
			else if(e.key==='ArrowLeft')moveDir('left');
			else if(e.key==='ArrowRight')moveDir('right');
		};
		document.addEventListener('keydown', keyHandler);

		render();
		window.ppSay(T('games.g14.hello'));
	}

	onDestroy(() => { if(keyHandler) document.removeEventListener('keydown', keyHandler); });
</script>

<GameShell gameNum={14} title="Laberinto" icon="🧭" initGame={initG14} />
