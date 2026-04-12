<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { onDestroy } from 'svelte';
	import { lerpParam } from '$lib/data.js';

	let g37AnimId = 0;
	onDestroy(() => { if (g37AnimId) { cancelAnimationFrame(g37AnimId); g37AnimId = 0; } });

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG37(cont, lv) {
		if (g37AnimId) { cancelAnimationFrame(g37AnimId); g37AnimId = 0; }
		const COLORS = [
			{name:'rojo',hex:'#E74C3C'},
			{name:'azul',hex:'#3498DB'},
			{name:'verde',hex:'#2ECC71'},
			{name:'amarillo',hex:'#F1C40F'},
			{name:'morado',hex:'#9B59B6'},
			{name:'naranja',hex:'#E67E22'},
		];
		const numColors = lerpParam(lv, 2, 5);
		const targetCount = lerpParam(lv, 5, 12);
		const speed = lerpParam(lv, 0.4, 1.2);
		const maxBubbles = lerpParam(lv, 8, 20);

		cont.innerHTML = `<div class="ins" id="g37ins"></div>
			<div class="g37-score" id="g37score">0 / ${targetCount}</div>
			<div class="g37-area" id="g37area" style="position:relative;width:100%;height:280px;overflow:hidden;border-radius:12px;background:#E8F6FF"></div>`;

		const activeColors = COLORS.slice(0, numColors);
		let targetColor = activeColors[Math.floor(Math.random()*activeColors.length)];
		let popped = 0;
		let alive = true;
		const area = /** @type {HTMLElement} */ (cont.querySelector('#g37area'));
		/** @type {{el:HTMLElement,y:number,speed:number}[]} */
		const bubbles = [];

		/** @type {HTMLElement} */ (cont.querySelector('#g37ins')).textContent = '¡Toca las burbujas ' + targetColor.name + 's!';
		/** @type {HTMLElement} */ (cont.querySelector('#g37ins')).style.color = targetColor.hex;

		function spawnBubble() {
			if (!alive) return;
			const col = activeColors[Math.floor(Math.random()*activeColors.length)];
			const size = 36 + Math.random()*20;
			const x = Math.random() * (area.clientWidth - size);
			const el = document.createElement('div');
			el.className = 'g37-bubble';
			el.style.cssText = `width:${size}px;height:${size}px;background:${col.hex};left:${x}px;bottom:-${size}px;position:absolute;border-radius:50%;cursor:pointer;opacity:0.85;transition:opacity 0.2s;`;
			el.dataset.color = col.name;

			const handleTap = (/** @type {Event} */ e) => {
				e.preventDefault();
				if (!alive || el.dataset.popped) return;
				if (col.name === targetColor.name) {
					el.dataset.popped = '1';
					el.style.opacity = '0';
					el.style.transform = 'scale(1.5)';
					window.ppBeep(600 + popped*30, .1);
					window.ppOnCorrect();
					popped++;
					/** @type {HTMLElement} */ (cont.querySelector('#g37score')).textContent = popped + ' / ' + targetCount;
					setTimeout(()=>el.remove(), 200);
					if (popped >= targetCount) {
						alive = false;
						const _lv = window.ppWin();
						window.ppCelebrate('¡Cazador de burbujas! 🫧', 3, () => initG37(cont, window.ppGetLevel()), _lv);
					}
				} else {
					el.classList.add('err');
					setTimeout(()=>el.classList.remove('err'), 300);
					window.ppOnWrong(); window.ppBoo();
				}
			};
			el.addEventListener('click', handleTap);
			el.addEventListener('touchstart', handleTap, {passive:false});

			area.appendChild(el);
			bubbles.push({el, y: -size, speed: speed*(0.5+Math.random())});
		}

		let lastTime = 0;
		let spawnTimer = 0;
		/** @param {number} ts */
		function animate(ts) {
			if (!alive) return;
			const dt = lastTime ? (ts-lastTime)/16 : 1;
			lastTime = ts;
			spawnTimer += dt;
			if (spawnTimer > (60/(maxBubbles*speed)) && area.children.length < maxBubbles) {
				spawnBubble();
				spawnTimer = 0;
			}
			bubbles.forEach(b => {
				b.y += b.speed * dt;
				b.el.style.bottom = b.y + 'px';
				if (b.y > area.clientHeight + 50) { b.el.remove(); }
			});
			// cleanup
			for (let i=bubbles.length-1;i>=0;i--) {
				if (!bubbles[i].el.parentNode) bubbles.splice(i,1);
			}
			g37AnimId = requestAnimationFrame(animate);
		}
		g37AnimId = requestAnimationFrame(animate);
		window.ppSay('¡Toca las burbujas de color ' + targetColor.name + '!');
	}
</script>

<GameShell gameNum={37} title="Burbujas" icon="🫧" initGame={initG37} />
