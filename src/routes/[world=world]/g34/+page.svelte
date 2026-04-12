<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam } from '$lib/data.js';

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG34(cont, lv) {
		let round = 0;
		const total = lerpParam(lv, 4, 7);

		cont.innerHTML = `<div class="ins">¡Repite el ritmo!</div>
			<div class="pbar"><div class="pfill" id="g34pb" style="width:0%;background:var(--c5)"></div></div>
			<div class="g34-display" id="g34disp"></div>
			<div class="g34-pad" id="g34pad"></div>
			<div class="g34-status" id="g34st"></div>`;

		const padColors = ['#E74C3C','#3498DB','#2ECC71','#F39C12'];
		const numPads = lv<=3?2:lv<=7?3:4;
		const seqLen = lerpParam(lv, 3, 7);

		function next() {
			if (round >= total) { const _lv = window.ppWin(); window.ppCelebrate('¡Gran sentido del ritmo! 🥁', 3, () => initG34(cont, window.ppGetLevel()), _lv); return; }
			/** @type {HTMLElement} */ (cont.querySelector('#g34pb')).style.width = (round/total*100)+'%';

			// generate sequence
			/** @type {number[]} */
			const seq = [];
			for (let i=0; i<seqLen; i++) seq.push(Math.floor(Math.random()*numPads));

			let inputIdx = 0;
			let listening = false;

			const padEl = /** @type {HTMLElement} */ (cont.querySelector('#g34pad')); padEl.innerHTML='';
			/** @type {HTMLElement[]} */
			const pads = [];
			for (let i=0;i<numPads;i++){
				const p = document.createElement('div');
				p.className='g34-btn';
				p.style.background = padColors[i];
				p.onclick = () => {
					if (!listening) return;
					flashPad(i);
					playTone(i);
					if (seq[inputIdx]===i) {
						inputIdx++;
						if (inputIdx>=seq.length) {
							listening = false;
							/** @type {HTMLElement} */ (cont.querySelector('#g34st')).textContent = '¡Perfecto! 🎉';
							window.ppBeep(880,.2);
							window.ppOnCorrect();
							round++;
							setTimeout(next, 1000);
						}
					} else {
						listening = false;
						/** @type {HTMLElement} */ (cont.querySelector('#g34st')).textContent = '¡Inténtalo de nuevo!';
						window.ppOnWrong(); window.ppBoo();
						setTimeout(() => playSequence(), 1000);
					}
				};
				pads.push(p);
				padEl.appendChild(p);
			}

			/** @param {number} idx */
			function flashPad(idx) {
				pads[idx].style.opacity='0.4';
				setTimeout(()=>pads[idx].style.opacity='1', 200);
			}

			/** @param {number} idx */
			function playTone(idx) {
				window.ppBeep(300 + idx * 150, 0.15, 'sine', 0.3);
			}

			function playSequence() {
				listening = false;
				inputIdx = 0;
				/** @type {HTMLElement} */ (cont.querySelector('#g34st')).textContent = '👀 Observa...';
				seq.forEach((s, i) => {
					setTimeout(()=>{
						flashPad(s);
						playTone(s);
					}, i*500);
				});
				setTimeout(()=>{
					listening = true;
					/** @type {HTMLElement} */ (cont.querySelector('#g34st')).textContent = '🎵 ¡Tu turno!';
				}, seq.length*500+300);
			}

			playSequence();
		}
		window.ppSay('¡Escucha y repite el ritmo!');
		next();
	}
</script>

<GameShell gameNum={34} title="Ritmo" icon="🥁" initGame={initG34} />
