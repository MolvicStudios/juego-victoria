<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	const T = (key, vars) => window.ppT?.(key, vars) ?? key;

	const G21_WORDS=[
		{k:'sol',e:'☀️'},{k:'pan',e:'🍞'},{k:'luz',e:'💡'},{k:'mar',e:'🌊'},
		{k:'gato',e:'🐱'},{k:'luna',e:'🌙'},{k:'casa',e:'🏠'},{k:'mesa',e:'🪑'},
		{k:'perro',e:'🐶'},{k:'flor',e:'🌸'},{k:'arbol',e:'🌳'},{k:'nube',e:'☁️'},
		{k:'pelota',e:'⚽'},{k:'camisa',e:'👔'},{k:'zapato',e:'👟'},{k:'tomate',e:'🍅'},
		{k:'estrella',e:'⭐'},{k:'mariposa',e:'🦋'},{k:'elefante',e:'🐘'},
	];

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG21(cont, lv) {
		let round = 0;
		const maxLen = lv<=3?3:lv<=6?4:lv<=9?5:lv<=12?6:8;
		const pool = G21_WORDS.filter(d => T('games.g21.words.'+d.k).length <= maxLen);
		const data = shuf(pool).slice(0, lerpParam(lv, 4, 7));

		cont.innerHTML = `<div class="ins">${T('games.g21.instruction')}</div>
			<div class="pbar"><div class="pfill" id="g21pb" style="width:0%;background:var(--c4)"></div></div>
			<div class="g8-emo" id="g21emo"></div>
			<div class="g21-target" id="g21target"></div>
			<div class="g21-letters" id="g21letters"></div>`;

		function next() {
			if (round >= data.length) { const _lv = window.ppWin(); window.ppCelebrate(T('games.g21.win'), 3, () => initG21(cont, window.ppGetLevel()), _lv); return; }
			/** @type {HTMLElement} */ (cont.querySelector('#g21pb')).style.width = (round/data.length*100)+'%';
			const d = data[round];
			const word = T('games.g21.words.'+d.k);
			/** @type {HTMLElement} */ (cont.querySelector('#g21emo')).textContent = d.e;
			let placed = 0;
			const targetEl = /** @type {HTMLElement} */ (cont.querySelector('#g21target')); targetEl.innerHTML = '';
			const lettersEl = /** @type {HTMLElement} */ (cont.querySelector('#g21letters')); lettersEl.innerHTML = '';

			const letters = word.split('');
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
						if (placed >= letters.length) { window.ppOnCorrect(); round++; setTimeout(next, 900); window.ppSay(T('games.g21.correct', {word})); }
					} else {
						b.classList.add('err'); setTimeout(()=>b.classList.remove('err'),400);
						window.ppOnWrong(); window.ppBoo(); window.ppSay(T('games.g21.wrong_letter'));
					}
				};
				lettersEl.appendChild(b);
			});
			window.ppSay(T('games.g21.question', {word: word.toLowerCase()}));
		}
		next();
	}
</script>

<GameShell gameNum={21} title="Deletrear" icon="🔤" initGame={initG21} />
