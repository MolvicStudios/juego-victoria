<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	const G21_WORDS=[
		{w:'SOL',e:'☀️'},{w:'PAN',e:'🍞'},{w:'LUZ',e:'💡'},{w:'MAR',e:'🌊'},
		{w:'GATO',e:'🐱'},{w:'LUNA',e:'🌙'},{w:'CASA',e:'🏠'},{w:'MESA',e:'🪑'},
		{w:'PERRO',e:'🐶'},{w:'FLOR',e:'🌸'},{w:'ÁRBOL',e:'🌳'},{w:'NUBE',e:'☁️'},
		{w:'PELOTA',e:'⚽'},{w:'CAMISA',e:'👔'},{w:'ZAPATO',e:'👟'},{w:'TOMATE',e:'🍅'},
		{w:'ESTRELLA',e:'⭐'},{w:'MARIPOSA',e:'🦋'},{w:'ELEFANTE',e:'🐘'},
	];

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG21(cont, lv) {
		let round = 0;
		const maxLen = lv<=3?3:lv<=6?4:lv<=9?5:lv<=12?6:8;
		const pool = G21_WORDS.filter(d => d.w.length <= maxLen);
		const data = shuf(pool).slice(0, lerpParam(lv, 4, 7));

		cont.innerHTML = `<div class="ins">¡Ordena las letras para formar la palabra!</div>
			<div class="pbar"><div class="pfill" id="g21pb" style="width:0%;background:var(--c4)"></div></div>
			<div class="g8-emo" id="g21emo"></div>
			<div class="g21-target" id="g21target"></div>
			<div class="g21-letters" id="g21letters"></div>`;

		function next() {
			if (round >= data.length) { const _lv = window.ppWin(); window.ppCelebrate('¡Deletreas genial! 🔤', 3, () => initG21(cont, window.ppGetLevel()), _lv); return; }
			/** @type {HTMLElement} */ (cont.querySelector('#g21pb')).style.width = (round/data.length*100)+'%';
			const d = data[round];
			/** @type {HTMLElement} */ (cont.querySelector('#g21emo')).textContent = d.e;
			let placed = 0;
			const targetEl = /** @type {HTMLElement} */ (cont.querySelector('#g21target')); targetEl.innerHTML = '';
			const lettersEl = /** @type {HTMLElement} */ (cont.querySelector('#g21letters')); lettersEl.innerHTML = '';

			const letters = d.w.split('');
			/** @type {HTMLDivElement[]} */
			const slots = [];
			letters.forEach((_, i) => {
				const s = document.createElement('div'); s.className = 'g21-slot'; s.dataset.idx = String(i);
				targetEl.appendChild(s); slots.push(s);
			});

			if (lv <= 3) { slots[0].textContent = letters[0]; slots[0].classList.add('filled'); placed = 1; }

			shuf(lv<=3 ? letters.slice(1) : [...letters]).forEach(ch => {
				const b = document.createElement('button'); b.className = 'g21-letter'; b.textContent = ch;
				b.onclick = () => {
					if (b.classList.contains('used')) return;
					const nextSlot = slots.find(s => !s.classList.contains('filled'));
					if (!nextSlot) return;
					const idx = parseInt(nextSlot.dataset.idx || '0');
					if (ch === letters[idx]) {
						nextSlot.textContent = ch; nextSlot.classList.add('filled'); b.classList.add('used');
						window.ppBeep(400+placed*80,.12); window.ppSay(ch); placed++;
						if (placed >= letters.length) { window.ppOnCorrect(); round++; setTimeout(next, 900); window.ppSay('¡'+d.w+'! ¡Muy bien!'); }
					} else {
						b.classList.add('err'); setTimeout(()=>b.classList.remove('err'),400);
						window.ppOnWrong(); window.ppBoo(); window.ppSay('¡Esa letra no va ahí!');
					}
				};
				lettersEl.appendChild(b);
			});
			window.ppSay('¿Cómo se escribe '+d.w.toLowerCase()+'?');
		}
		next();
	}
</script>

<GameShell gameNum={21} title="Deletrear" icon="🔤" initGame={initG21} />
