<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	const T = (key, vars) => window.ppT?.(key, vars) ?? key;

	const G23_DATA=[
		{k:'s1'},{k:'s2'},{k:'s3'},{k:'s4'},{k:'s5'},
		{k:'s6'},{k:'s7'},{k:'s8'},{k:'s9'},{k:'s10'},
		{k:'s11'},{k:'s12'},{k:'s13'},{k:'s14'},{k:'s15'},
	];

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG23(cont, lv) {
		let round = 0;
		const data = shuf(G23_DATA).slice(0, lerpParam(lv, 5, 8));

		cont.innerHTML = `<div class="ins">${T('games.g23.instruction')}</div>
			<div class="pbar"><div class="pfill" id="g23pb" style="width:0%;background:var(--c6)"></div></div>
			<div class="g23-frase" id="g23frase"></div>
			<div class="g8-opts" id="g23opts"></div>`;

		function next() {
			if (round >= data.length) { const _lv = window.ppWin(); window.ppCelebrate(T('games.g23.win'), 3, () => initG23(cont, window.ppGetLevel()), _lv); return; }
			/** @type {HTMLElement} */ (cont.querySelector('#g23pb')).style.width = (round/data.length*100)+'%';
			const d = data[round];
			const frame = T('games.g23.'+d.k+'.f');
			const answer = T('games.g23.'+d.k+'.a');
			/** @type {HTMLElement} */ (cont.querySelector('#g23frase')).textContent = frame;
			const numOpts = lv<=3?2:lv<=7?3:4;
			const wrongs = [];
			for (let i = 1; i <= 3 && wrongs.length < numOpts-1; i++) wrongs.push(T('games.g23.'+d.k+'.x'+i));
			const optsEl = /** @type {HTMLElement} */ (cont.querySelector('#g23opts')); optsEl.innerHTML = '';
			shuf([answer, ...wrongs]).forEach(c => {
				const b = document.createElement('div'); b.className = 'g8-opt'; b.textContent = c;
				b.onclick = () => {
					if(c===answer){b.style.background='#EFFFEF';b.style.borderColor='#6BCB77';window.ppBeep(880,.2);window.ppSay(T('games.g23.correct', {sentence: frame.replace('___',answer)}));window.ppOnCorrect();round++;setTimeout(next,1200);}
					else{b.classList.add('err');setTimeout(()=>b.classList.remove('err'),400);window.ppOnWrong();window.ppBoo();window.ppSay(T('games.common.try_again'));}
				};
				optsEl.appendChild(b);
			});
			window.ppSay(frame.replace('___',T('games.g23.question_what')));
		}
		next();
	}
</script>

<GameShell gameNum={23} title="Completa Frase" icon="💬" initGame={initG23} />
