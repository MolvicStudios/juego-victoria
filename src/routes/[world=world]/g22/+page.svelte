<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	/** @type {(key: string, vars?: Record<string, string|number>) => string} */ const T = (key, vars) => window.ppT?.(key, vars) ?? key;

	const G22_DATA=[
		{a:'big',b:'small',e:'🐘↔🐭'},{a:'hot',b:'cold',e:'🔥↔❄️'},
		{a:'fast',b:'slow',e:'🐇↔🐢'},{a:'tall',b:'short_h',e:'🦒↔🐁'},
		{a:'day',b:'night',e:'☀️↔🌙'},{a:'happy',b:'sad',e:'😊↔😢'},
		{a:'full',b:'empty',e:'🥛↔🫧'},{a:'open',b:'closed',e:'📖↔📕'},
		{a:'new',b:'old',e:'✨↔🏠️'},{a:'soft',b:'hard',e:'☁️↔🪨'},
		{a:'up',b:'down',e:'⬆️↔⬇️'},{a:'light',b:'dark',e:'💡↔🌑'},
		{a:'long',b:'short_l',e:'🐍↔🐛'},{a:'fat',b:'thin',e:'🐷↔🦩'},
		{a:'clean',b:'dirty',e:'🧼↔🗑️'},{a:'strong',b:'weak',e:'💪↔🪶'},
	];

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG22(cont, lv) {
		let round = 0;
		const data = shuf(G22_DATA).slice(0, lerpParam(lv, 5, 8));

		cont.innerHTML = `<div class="ins">${T('games.g22.instruction')}</div>
			<div class="pbar"><div class="pfill" id="g22pb" style="width:0%;background:var(--c2)"></div></div>
			<div class="g22-prompt" id="g22prompt"></div>
			<div class="g8-opts" id="g22opts"></div>`;

		function next() {
			if (round >= data.length) { const _lv = window.ppWin(); window.ppCelebrate(T('games.g22.win'), 3, () => initG22(cont, window.ppGetLevel()), _lv); return; }
			/** @type {HTMLElement} */ (cont.querySelector('#g22pb')).style.width = (round/data.length*100)+'%';
			const d = data[round];
			const wText = T('games.g22.pairs.'+d.a);
			const oText = T('games.g22.pairs.'+d.b);
			const promptEl = /** @type {HTMLElement} */ (cont.querySelector('#g22prompt'));
			promptEl.innerHTML = '<div style="font-size:2.5rem;margin-bottom:8px">'+d.e.split('↔')[0]+'</div><div style="font-size:1.8rem;font-weight:900">'+wText+'</div><div style="font-size:.8rem;color:var(--ink2);margin-top:4px">'+T('games.g22.q_label')+'</div>';
			const numOpts = lv<=3?2:lv<=7?3:4;
			const others = G22_DATA.filter(x => x.b !== d.b && x.a !== d.b).map(x => T('games.g22.pairs.'+x.b));
			const wrongs = shuf(others).slice(0, numOpts-1);
			const optsEl = /** @type {HTMLElement} */ (cont.querySelector('#g22opts')); optsEl.innerHTML = '';
			shuf([oText, ...wrongs]).forEach(c => {
				const b = document.createElement('div'); b.className = 'g8-opt'; b.textContent = c;
				b.onclick = () => {
					if(c===oText){b.style.background='#EFFFEF';b.style.borderColor='#6BCB77';window.ppBeep(880,.2);window.ppSay(T('games.g22.correct', {word: wText, opposite: oText}));window.ppOnCorrect();round++;setTimeout(next,1100);}
					else{b.classList.add('err');setTimeout(()=>b.classList.remove('err'),400);window.ppOnWrong();window.ppBoo();window.ppSay(T('games.common.try_again'));}
				};
				optsEl.appendChild(b);
			});
			window.ppSay(T('games.g22.question', {word: wText}));
		}
		next();
	}
</script>

<GameShell gameNum={22} title="Opuestos" icon="↔️" initGame={initG22} />
