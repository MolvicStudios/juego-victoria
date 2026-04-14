<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	/** @type {(key: string, vars?: Record<string, string|number>) => string} */ const T = (key, vars) => window.ppT?.(key, vars) ?? key;

	const G20_DATA=[
		{w:'gato',r:'pato',x:['perro','casa','sol']},
		{w:'luna',r:'cuna',x:['nube','gato','mesa']},
		{w:'raton',r:'balon',x:['casa','perro','luna']},
		{w:'flor',r:'color',x:['mesa','gato','nube']},
		{w:'estrella',r:'botella',x:['mesa','gato','luna']},
		{w:'camion',r:'avion',x:['casa','perro','mesa']},
		{w:'zapato',r:'plato',x:['luna','sol','nube']},
		{w:'cancion',r:'corazon',x:['mesa','perro','casa']},
		{w:'campana',r:'manzana',x:['gato','sol','perro']},
		{w:'silla',r:'ardilla',x:['luna','mesa','casa']},
		{w:'conejo',r:'espejo',x:['gato','sol','nube']},
		{w:'tortuga',r:'lechuga',x:['perro','luna','mesa']},
		{w:'coche',r:'noche',x:['gato','casa','sol']},
		{w:'piso',r:'aviso',x:['luna','perro','mesa']},
		{w:'ballena',r:'arena',x:['gato','sol','casa']},
	];

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG20(cont, lv) {
		let round = 0;
		const data = shuf(G20_DATA).slice(0, lerpParam(lv, 5, 8));

		cont.innerHTML = `<div class="ins">${T('games.g20.instruction')}</div>
			<div class="pbar"><div class="pfill" id="g20pb" style="width:0%;background:var(--c5)"></div></div>
			<div class="g3-letter" id="g20word" style="font-size:2.8rem"></div>
			<div class="g8-opts" id="g20opts"></div>`;

		function next() {
			if (round >= data.length) { const _lv = window.ppWin(); window.ppCelebrate(T('games.g20.win')+' 🎤', 3, () => initG20(cont, window.ppGetLevel()), _lv); return; }
			/** @type {HTMLElement} */ (cont.querySelector('#g20pb')).style.width = (round/data.length*100)+'%';
			const d = data[round];
			/** @type {HTMLElement} */ (cont.querySelector('#g20word')).textContent = '🎤 ' + T('games.g20.words.'+d.w);
			const numWrong = lv<=3?1:lv<=7?2:3;
			const wrongs = d.x.slice(0, numWrong);
			const optsEl = /** @type {HTMLElement} */ (cont.querySelector('#g20opts')); optsEl.innerHTML = '';
			shuf([d.r, ...wrongs]).forEach(c => {
				const b = document.createElement('div'); b.className = 'g8-opt'; b.textContent = c===d.r ? T('games.g20.rhymes.'+c) : T('games.g20.wrong.'+c);
				b.onclick = () => {
					if(c===d.r){b.style.background='#EFFFEF';b.style.borderColor='#6BCB77';window.ppBeep(880,.2);window.ppSay(T('games.g20.correct',{word:T('games.g20.words.'+d.w),rhyme:T('games.g20.rhymes.'+d.r)}));window.ppOnCorrect();round++;setTimeout(next,1100);}
					else{b.classList.add('err');setTimeout(()=>b.classList.remove('err'),400);window.ppOnWrong();window.ppBoo();window.ppSay(T('games.common.try_again'));}
				};
				optsEl.appendChild(b);
			});
			window.ppSay(T('games.g20.question',{word:T('games.g20.words.'+d.w)}));
		}
		next();
	}
</script>

<GameShell gameNum={20} title="Rimas" icon="🎤" initGame={initG20} />
