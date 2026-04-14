<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	const T = (key, vars) => window.ppT?.(key, vars) ?? key;

	/** @typedef {{key: string, draw: (ctx: CanvasRenderingContext2D, cx: number, cy: number, s: number) => void}} G30Shape */
	/** @type {G30Shape[]} */
	const SHAPES = [
		{key:'star', draw:(ctx,cx,cy,s)=>{ctx.beginPath();for(let i=0;i<5;i++){const a=(i*72-90)*Math.PI/180;const b=((i*72)+36-90)*Math.PI/180;ctx.lineTo(cx+Math.cos(a)*s,cy+Math.sin(a)*s);ctx.lineTo(cx+Math.cos(b)*s*0.4,cy+Math.sin(b)*s*0.4);}ctx.closePath();}},
		{key:'heart', draw:(ctx,cx,cy,s)=>{ctx.beginPath();ctx.moveTo(cx,cy+s*0.6);ctx.bezierCurveTo(cx-s,cy-s*0.2,cx-s*0.5,cy-s,cx,cy-s*0.4);ctx.bezierCurveTo(cx+s*0.5,cy-s,cx+s,cy-s*0.2,cx,cy+s*0.6);ctx.closePath();}},
		{key:'house', draw:(ctx,cx,cy,s)=>{ctx.beginPath();ctx.moveTo(cx-s*0.6,cy+s*0.6);ctx.lineTo(cx-s*0.6,cy-s*0.1);ctx.lineTo(cx,cy-s*0.7);ctx.lineTo(cx+s*0.6,cy-s*0.1);ctx.lineTo(cx+s*0.6,cy+s*0.6);ctx.closePath();}},
		{key:'arrow', draw:(ctx,cx,cy,s)=>{ctx.beginPath();ctx.moveTo(cx,cy-s*0.8);ctx.lineTo(cx+s*0.5,cy);ctx.lineTo(cx+s*0.2,cy);ctx.lineTo(cx+s*0.2,cy+s*0.6);ctx.lineTo(cx-s*0.2,cy+s*0.6);ctx.lineTo(cx-s*0.2,cy);ctx.lineTo(cx-s*0.5,cy);ctx.closePath();}},
		{key:'moon', draw:(ctx,cx,cy,s)=>{ctx.beginPath();ctx.arc(cx,cy,s,0,Math.PI*2);ctx.moveTo(cx+s*0.4,cy);ctx.arc(cx+s*0.4,cy,s*0.75,0,Math.PI*2,true);ctx.closePath();}},
		{key:'diamond', draw:(ctx,cx,cy,s)=>{ctx.beginPath();ctx.moveTo(cx,cy-s);ctx.lineTo(cx+s*0.6,cy);ctx.lineTo(cx,cy+s);ctx.lineTo(cx-s*0.6,cy);ctx.closePath();}},
		{key:'cross', draw:(ctx,cx,cy,s)=>{const w=s*0.3;ctx.beginPath();ctx.rect(cx-w,cy-s*0.7,w*2,s*1.4);ctx.rect(cx-s*0.7,cy-w,s*1.4,w*2);ctx.closePath();}},
		{key:'lightning', draw:(ctx,cx,cy,s)=>{ctx.beginPath();ctx.moveTo(cx+s*0.1,cy-s*0.8);ctx.lineTo(cx-s*0.3,cy);ctx.lineTo(cx+s*0.05,cy);ctx.lineTo(cx-s*0.1,cy+s*0.8);ctx.lineTo(cx+s*0.3,cy);ctx.lineTo(cx-s*0.05,cy);ctx.closePath();}},
	];

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG30(cont, lv) {
		let round = 0;
		const pool = shuf(SHAPES).slice(0, lerpParam(lv, 4, 7));
		const total = pool.length;

		cont.innerHTML = `<div class="ins">${T('games.g30.instruction')}</div>
			<div class="pbar"><div class="pfill" id="g30pb" style="width:0%;background:var(--c2)"></div></div>
			<canvas id="g30shadow" width="120" height="120" style="display:block;margin:8px auto;background:#f0f0f0;border-radius:12px"></canvas>
			<div class="g30-opts" id="g30opts"></div>`;

		/** @param {HTMLCanvasElement} cvs @param {G30Shape} shape @param {string} color */
		function drawShape(cvs, shape, color) {
			const ctx = cvs.getContext('2d');
			if (!ctx) return;
			ctx.clearRect(0,0,cvs.width,cvs.height);
			ctx.fillStyle = color;
			shape.draw(ctx, cvs.width/2, cvs.height/2, cvs.width*0.35);
			ctx.fill();
		}

		function next() {
			if (round >= total) { const _lv = window.ppWin(); window.ppCelebrate(T('games.g30.win'), 3, () => initG30(cont, window.ppGetLevel()), _lv); return; }
			/** @type {HTMLElement} */ (cont.querySelector('#g30pb')).style.width = (round/total*100)+'%';

			const target = pool[round];
			const shadow = /** @type {HTMLCanvasElement} */ (cont.querySelector('#g30shadow'));
			drawShape(shadow, target, '#333');

			const numOpts = lv<=3?2:lv<=7?3:4;
			const others = SHAPES.filter(s=>s.key!==target.key);
			const wrongs = shuf(others).slice(0, numOpts-1);
			const opts = shuf([target, ...wrongs]);

			const optsEl = /** @type {HTMLElement} */ (cont.querySelector('#g30opts')); optsEl.innerHTML='';
			opts.forEach(s => {
				const c = document.createElement('canvas');
				c.width=80; c.height=80; c.className='g30-opt';
				optsEl.appendChild(c);
				const colors = ['#E74C3C','#3498DB','#2ECC71','#F39C12','#9B59B6','#1ABC9C'];
				drawShape(c, s, colors[Math.floor(Math.random()*colors.length)]);
				c.onclick = () => {
					if(s.key===target.key){c.style.border='3px solid #6BCB77';window.ppBeep(880,.2);window.ppSay(T('games.g30.correct', {name: T('games.g30.shapes.' + target.key)}));window.ppOnCorrect();round++;setTimeout(next,1000);}
					else{c.classList.add('err');setTimeout(()=>c.classList.remove('err'),400);window.ppOnWrong();window.ppBoo();}
				};
			});
			window.ppSay(T('games.g30.hello'));
		}
		next();
	}
</script>

<GameShell gameNum={30} title="Sombras" icon="👤" initGame={initG30} />
