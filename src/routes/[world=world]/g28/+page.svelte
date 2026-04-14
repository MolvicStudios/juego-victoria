<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	const T = (key, vars) => window.ppT?.(key, vars) ?? key;

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG28(cont, lv) {
		let round = 0;
		const total = lerpParam(lv, 5, 8);
		const showMinutes = lv >= 4;
		const minuteStep = lv <= 6 ? 30 : lv <= 10 ? 15 : 5;

		cont.innerHTML = `<div class="ins">${T('games.g28.instruction')}</div>
			<div class="pbar"><div class="pfill" id="g28pb" style="width:0%;background:var(--c6)"></div></div>
			<canvas id="g28cvs" style="display:block;margin:0 auto;width:200px;height:200px"></canvas>
			<div class="g8-opts" id="g28opts"></div>`;

		/** @param {HTMLCanvasElement} cvs @param {number} h @param {number} m */
		function drawClock(cvs, h, m) {
			const dpr = window.devicePixelRatio || 1;
			cvs.width = 200 * dpr; cvs.height = 200 * dpr;
			const ctx = cvs.getContext('2d');
			if (!ctx) return;
			ctx.scale(dpr, dpr);
			const cx = 100, cy = 100, r = 90;
			ctx.clearRect(0,0,200,200);

			// face
			ctx.beginPath(); ctx.arc(cx,cy,r,0,Math.PI*2); ctx.fillStyle='#FFF'; ctx.fill();
			ctx.strokeStyle='#333'; ctx.lineWidth=3; ctx.stroke();

			// numbers
			ctx.fillStyle='#333'; ctx.font='bold 16px sans-serif'; ctx.textAlign='center'; ctx.textBaseline='middle';
			for (let i=1;i<=12;i++) {
				const a = (i*30-90)*Math.PI/180;
				ctx.fillText(String(i), cx+Math.cos(a)*(r-20), cy+Math.sin(a)*(r-20));
			}

			// hour hand
			const ha = ((h%12)+m/60)*30-90;
			const hr = ha*Math.PI/180;
			ctx.beginPath(); ctx.moveTo(cx,cy);
			ctx.lineTo(cx+Math.cos(hr)*(r*0.5), cy+Math.sin(hr)*(r*0.5));
			ctx.strokeStyle='#333'; ctx.lineWidth=4; ctx.lineCap='round'; ctx.stroke();

			// minute hand
			const ma = (m*6-90)*Math.PI/180;
			ctx.beginPath(); ctx.moveTo(cx,cy);
			ctx.lineTo(cx+Math.cos(ma)*(r*0.7), cy+Math.sin(ma)*(r*0.7));
			ctx.strokeStyle='#E74C3C'; ctx.lineWidth=2; ctx.stroke();

			// center dot
			ctx.beginPath(); ctx.arc(cx,cy,4,0,Math.PI*2); ctx.fillStyle='#333'; ctx.fill();
		}

		/** @param {number} h @param {number} m */
		function fmtTime(h,m) {
			return h + ':' + (m<10?'0':'') + m;
		}

		function next() {
			if (round >= total) { const _lv = window.ppWin(); window.ppCelebrate(T('games.g28.win'), 3, () => initG28(cont, window.ppGetLevel()), _lv); return; }
			/** @type {HTMLElement} */ (cont.querySelector('#g28pb')).style.width = (round/total*100)+'%';

			const h = Math.floor(Math.random()*12)+1;
			const m = showMinutes ? Math.floor(Math.random()*(60/minuteStep))*minuteStep : 0;
			const cvs = /** @type {HTMLCanvasElement} */ (cont.querySelector('#g28cvs'));
			drawClock(cvs, h, m);

			const ans = fmtTime(h,m);
			const numOpts = lv<=3?2:lv<=7?3:4;
			const wrongs = new Set();
			let guard = 0;
			while(wrongs.size < numOpts-1 && guard < 100) {
				guard++;
				let wh = h + (Math.random()<0.5?1:-1)*(Math.floor(Math.random()*3)+1);
				if(wh<1) wh=12; if(wh>12) wh=wh%12||12;
				let wm = showMinutes ? Math.floor(Math.random()*(60/minuteStep))*minuteStep : 0;
				const wt = fmtTime(wh,wm);
				if(wt!==ans && !wrongs.has(wt)) wrongs.add(wt);
			}

			const optsEl = /** @type {HTMLElement} */ (cont.querySelector('#g28opts')); optsEl.innerHTML='';
			shuf([ans,...wrongs]).forEach(t => {
				const b = document.createElement('div');
				b.className = 'g8-opt'; b.textContent = t;
				b.onclick = () => {
					if(t===ans){b.style.background='#EFFFEF';b.style.borderColor='#6BCB77';window.ppBeep(880,.2);window.ppSay(m>0?T('games.g28.correct_min',{h,m}):T('games.g28.correct',{h}));window.ppOnCorrect();round++;setTimeout(next,1200);}
					else{b.classList.add('err');setTimeout(()=>b.classList.remove('err'),400);window.ppOnWrong();window.ppBoo();window.ppSay(T('games.common.try_again'));}
				};
				optsEl.appendChild(b);
			});
			window.ppSay(T('games.g28.hello'));
		}
		next();
	}
</script>

<GameShell gameNum={28} title="El Reloj" icon="⏰" initGame={initG28} />
