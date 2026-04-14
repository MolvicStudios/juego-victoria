<script>
	import GameShell from '$lib/components/GameShell.svelte';
	const T = (key, vars) => window.ppT?.(key, vars) ?? key;

	const G4_COLS=['#FF6B6B','#FF9F43','#FFD93D','#6BCB77','#38B2AC','#4D9FEC','#A78BFA','#F472B6','#2D3748','#ffffff','#8B5CF6','#EC4899','#14B8A6','#F59E0B','#3B82F6','#EF4444'];
	const G4_STMP=['🌸','⭐','❤️','🦋','🐱','🐶','🌈','🎈','🍎','🌟'];
	let g4Color='#FF6B6B',g4Size=8,g4Drawing=false,g4lx=0,g4ly=0,g4Mode='brush',g4Stamp='🌸',container;

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG4(cont, lv) {
		container = cont; g4Mode = 'brush'; g4Stamp = '🌸';
		const numCols = lv<=3?6:lv<=7?10:lv<=11?12:16;
		cont.innerHTML = `<canvas id="g4cvs"></canvas><div class="g4-pal" id="g4pal"></div><div class="g4-tools" id="g4tools"></div><div class="g4-stamps" id="g4stamps" style="display:none"></div>`;
		cont.style.gap = '6px'; cont.style.padding = '8px';

		const cvs = /** @type {HTMLCanvasElement} */ (cont.querySelector('#g4cvs'));
		const W = Math.min(cont.clientWidth-16, 500), H = Math.min(window.innerHeight-280, 320);
		cvs.width = W; cvs.height = H;
		const ctx = /** @type {CanvasRenderingContext2D} */ (cvs.getContext('2d')); ctx.fillStyle = '#fff'; ctx.fillRect(0,0,W,H);

		const palEl = /** @type {HTMLElement} */ (cont.querySelector('#g4pal')); palEl.innerHTML = '';
		G4_COLS.slice(0,numCols).forEach(c => {
			const d = document.createElement('div'); d.className = 'g4-dot'+(c===g4Color?' on':'');
			d.style.background = c; if(c==='#ffffff') d.style.border = '3px solid #DDD';
			d.onclick = () => { g4Color=c; palEl.querySelectorAll('.g4-dot').forEach(x=>x.classList.remove('on')); d.classList.add('on'); window.ppBeep(600,.06); };
			palEl.appendChild(d);
		});

		const toolsEl = /** @type {HTMLElement} */ (cont.querySelector('#g4tools')); toolsEl.innerHTML = '';
		const tools = [{id:'brush',label:'games.g4.tools.brush',minLv:1},{id:'stamp',label:'games.g4.tools.stamps',minLv:4},{id:'thin',label:'games.g4.tools.thin',minLv:1},{id:'thick',label:'games.g4.tools.thick',minLv:1},{id:'eraser',label:'games.g4.tools.erase',minLv:1}];
		tools.forEach(t => {
			if(lv<t.minLv) return;
			const b = document.createElement('button'); b.className = 'g4-tool'; b.textContent = T(t.label);
			b.onclick = () => {
				if(t.id==='eraser'){ctx.fillStyle='#fff';ctx.fillRect(0,0,cvs.width,cvs.height);window.ppBeep(400,.15);return;}
				if(t.id==='thin'){g4Size=4;return;} if(t.id==='thick'){g4Size=22;return;}
				if(t.id==='brush'){g4Mode='brush';/** @type {HTMLElement} */(cont.querySelector('#g4stamps')).style.display='none';return;}
				if(t.id==='stamp'){g4Mode='stamp';/** @type {HTMLElement} */(cont.querySelector('#g4stamps')).style.display='flex';return;}
			};
			toolsEl.appendChild(b);
		});

		const stampsEl = /** @type {HTMLElement} */ (cont.querySelector('#g4stamps')); stampsEl.innerHTML = '';
		G4_STMP.forEach(s => {
			const d = document.createElement('div'); d.className = 'g4-stamp'+(s===g4Stamp?' on':''); d.textContent = s;
			d.onclick = () => { g4Stamp=s; stampsEl.querySelectorAll('.g4-stamp').forEach(x=>x.classList.remove('on')); d.classList.add('on'); };
			stampsEl.appendChild(d);
		});

		/** @param {TouchEvent|MouseEvent} e */
		function pos(e){const r=cvs.getBoundingClientRect();const t='touches' in e?e.touches[0]:e;return[t.clientX-r.left,t.clientY-r.top];}
		/** @param {TouchEvent|MouseEvent} e */
		function start(e){e.preventDefault();g4Drawing=true;[g4lx,g4ly]=pos(e);
			if(g4Mode==='stamp'){ctx.font='32px serif';ctx.fillText(g4Stamp,g4lx-16,g4ly+12);window.ppBeep(600,.1);g4Drawing=false;return;}
		}
		/** @param {TouchEvent|MouseEvent} e */
		function draw(e){e.preventDefault();if(!g4Drawing)return;const[x,y]=pos(e);
			ctx.beginPath();ctx.moveTo(g4lx,g4ly);ctx.lineTo(x,y);
			ctx.strokeStyle=g4Color;ctx.lineWidth=g4Size;ctx.lineCap='round';ctx.lineJoin='round';ctx.stroke();
			[g4lx,g4ly]=[x,y];
		}
		function stop(){g4Drawing=false;}
		cvs.onmousedown=start;cvs.onmousemove=draw;cvs.onmouseup=stop;
		cvs.addEventListener('touchstart',/** @type {EventListener} */(start),{passive:false});
		cvs.addEventListener('touchmove',/** @type {EventListener} */(draw),{passive:false});
		cvs.addEventListener('touchend',stop);
		window.ppSay(T('games.g4.hello'));
	}
</script>

<GameShell gameNum={4} title="Pintar Libre" icon="🖌️" initGame={initG4} />
