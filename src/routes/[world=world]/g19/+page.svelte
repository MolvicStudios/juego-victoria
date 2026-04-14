<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	/** @type {(key: string, vars?: Record<string, string|number>) => string} */ const T = (key, vars) => window.ppT?.(key, vars) ?? key;

	const G19_DATA=[
		{w:'sol',s:1},{w:'mar',s:1},{w:'luz',s:1},{w:'pan',s:1},
		{w:'casa',s:2},{w:'mesa',s:2},{w:'luna',s:2},{w:'gato',s:2},{w:'perro',s:2},{w:'bota',s:2},
		{w:'pelota',s:3},{w:'mariposa',s:4},{w:'camisa',s:3},{w:'zapato',s:3},{w:'tomate',s:3},
		{w:'elefante',s:4},{w:'cocodrilo',s:4},{w:'dinosaurio',s:4},{w:'zanahoria',s:4},
		{w:'helicoptero',s:5},{w:'abecedario',s:5},{w:'rinoceronte',s:5},
	];

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG19(cont, lv) {
		let round = 0;
		const maxSyl = lv<=3?2:lv<=6?3:lv<=9?4:5;
		const pool = G19_DATA.filter(d => d.s <= maxSyl);
		const data = shuf(pool).slice(0, lerpParam(lv, 5, 8));

		cont.innerHTML = `<div class="ins">${T('games.g19.instruction')}</div>
			<div class="pbar"><div class="pfill" id="g19pb" style="width:0%;background:var(--c1)"></div></div>
			<div class="g3-letter" id="g19word" style="font-size:3rem"></div>
			<div class="g2-nums" id="g19opts" style="display:flex"></div>`;

		function next() {
			if (round >= data.length) { const _lv = window.ppWin(); window.ppCelebrate(T('games.g19.win')+' 👏', 3, () => initG19(cont, window.ppGetLevel()), _lv); return; }
			/** @type {HTMLElement} */ (cont.querySelector('#g19pb')).style.width = (round/data.length*100)+'%';
			const d = data[round];
			/** @type {HTMLElement} */ (cont.querySelector('#g19word')).textContent = T('games.g19.words.'+d.w);
			const numOpts = lv<=5?2:lv<=10?3:4;
			const cols = ['#FF6B6B','#4D9FEC','#6BCB77','#FF9F43'];
			const vals = [d.s]; let tries=0;
			while(vals.length<numOpts&&tries<50){tries++;const r=Math.max(1,d.s+Math.floor(Math.random()*5)-2);if(!vals.includes(r)&&r>=1&&r<=6)vals.push(r);}
			const optsEl = /** @type {HTMLElement} */ (cont.querySelector('#g19opts')); optsEl.innerHTML = '';
			shuf(vals).forEach((v,i) => {
				const b = document.createElement('button'); b.className = 'g2-num'; b.style.background = cols[i%4]; b.textContent = String(v);
				b.onclick = () => {
					if(v===d.s){b.style.background='#6BCB77';window.ppBeep(880,.2);window.ppSay(T('games.g19.correct',{word:T('games.g19.words.'+d.w),n:d.s,sylLabel:d.s===1?T('games.g19.syllable'):T('games.g19.syllables')}));window.ppOnCorrect();round++;setTimeout(next,1100);}
					else{b.classList.add('err');setTimeout(()=>b.classList.remove('err'),400);window.ppOnWrong();window.ppBoo();window.ppSay(T('games.common.try_again'));}
				};
				optsEl.appendChild(b);
			});
			window.ppSay(T('games.g19.question',{word:T('games.g19.words.'+d.w)}));
		}
		next();
	}
</script>

<GameShell gameNum={19} title="Sílabas" icon="👏" initGame={initG19} />
