<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam } from '$lib/data.js';

	const T = (key, vars) => window.ppT?.(key, vars) ?? key;

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG35(cont, lv) {
		const numDots = lerpParam(lv, 5, 15);

		cont.innerHTML = `<div class="ins">${T('games.g35.instruction')}</div>
			<canvas id="g35cvs" width="320" height="320" style="display:block;margin:0 auto;background:#FFFDE7;border-radius:12px;touch-action:none"></canvas>`;

		const cvs = /** @type {HTMLCanvasElement} */ (cont.querySelector('#g35cvs'));
		const ctx = /** @type {CanvasRenderingContext2D} */ (cvs.getContext('2d'));
		const DOT_R = 16;

		// Generate random dot positions (non-overlapping)
		/** @type {{x:number,y:number,n:number}[]} */
		const dots = [];
		const margin = 30;
		for (let i = 0; i < numDots; i++) {
			/** @type {number} */
			let x = 0;
			/** @type {number} */
			let y = 0;
			let ok, tries = 0;
			do {
				x = margin + Math.random() * (cvs.width - 2*margin);
				y = margin + Math.random() * (cvs.height - 2*margin);
				ok = dots.every(d => Math.hypot(d.x-x, d.y-y) > DOT_R*3);
				tries++;
			} while (!ok && tries < 100);
			dots.push({x, y, n: i+1});
		}

		let currentDot = 0;
		/** @type {{x:number,y:number,n:number}[]} */
		const connected = [];

		function draw() {
			ctx.clearRect(0,0,cvs.width,cvs.height);

			// draw lines between connected dots
			if (connected.length > 1) {
				ctx.beginPath();
				ctx.moveTo(connected[0].x, connected[0].y);
				for (let i=1;i<connected.length;i++) ctx.lineTo(connected[i].x, connected[i].y);
				ctx.strokeStyle='#3498DB'; ctx.lineWidth=3; ctx.lineCap='round'; ctx.stroke();
			}

			// draw dots
			dots.forEach((d,i) => {
				const isConnected = i < currentDot;
				const isCurrent = i === currentDot;
				ctx.beginPath();
				ctx.arc(d.x, d.y, DOT_R, 0, Math.PI*2);
				ctx.fillStyle = isConnected ? '#6BCB77' : isCurrent ? '#E74C3C' : '#DDD';
				ctx.fill();
				ctx.strokeStyle = '#333'; ctx.lineWidth = 2; ctx.stroke();
				ctx.fillStyle = isConnected ? '#FFF' : '#333';
				ctx.font = 'bold 12px sans-serif';
				ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
				ctx.fillText(String(d.n), d.x, d.y);
			});
		}

		/** @param {number} ex @param {number} ey */
		function handleTap(ex, ey) {
			if (currentDot >= dots.length) return;
			const rect = cvs.getBoundingClientRect();
			const x = (ex - rect.left) * (cvs.width / rect.width);
			const y = (ey - rect.top) * (cvs.height / rect.height);
			const d = dots[currentDot];
			if (Math.hypot(x-d.x, y-d.y) < DOT_R * 1.5) {
				connected.push(d);
				currentDot++;
				window.ppBeep(400 + currentDot*40, .1);
				window.ppOnCorrect();
				draw();
				if (currentDot >= dots.length) {
					const _lv = window.ppWin();
					window.ppCelebrate(T('games.g35.win') + ' ✏️', 3, () => initG35(cont, window.ppGetLevel()), _lv);
				}
			} else {
				window.ppOnWrong(); window.ppBoo();
			}
		}

		cvs.addEventListener('click', (/** @type {MouseEvent} */ e) => handleTap(e.clientX, e.clientY));
		cvs.addEventListener('touchstart', (/** @type {TouchEvent} */ e) => {
			e.preventDefault();
			const t = e.touches[0];
			handleTap(t.clientX, t.clientY);
		}, {passive:false});

		draw();
		window.ppSay(T('games.g35.hello', {n: numDots}));
	}
</script>

<GameShell gameNum={35} title="Conecta Puntos" icon="✏️" initGame={initG35} />
