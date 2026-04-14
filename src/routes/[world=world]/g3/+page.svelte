<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { shuf, lerpParam } from '$lib/data.js';
	/** @type {(key: string, vars?: Record<string, string|number>) => string} */ const T = (key, vars) => window.ppT?.(key, vars) ?? key;

	const G3_DATA=[
		{l:'A',w:[{e:'🌳',n:'tree'},{e:'🌸',n:'flower'},{e:'🐶',n:'dog'},{e:'🌙',n:'moon'}],ok:'tree'},
		{l:'B',w:[{e:'⛵',n:'boat'},{e:'☀️',n:'sun'},{e:'🐘',n:'elephant'},{e:'🌈',n:'rainbow'}],ok:'boat'},
		{l:'C',w:[{e:'🏠',n:'house'},{e:'🌙',n:'moon'},{e:'🐶',n:'dog'},{e:'🌸',n:'flower'}],ok:'house'},
		{l:'D',w:[{e:'🐬',n:'dolphin'},{e:'⭐',n:'star'},{e:'🌸',n:'flower'},{e:'🐱',n:'cat'}],ok:'dolphin'},
		{l:'E',w:[{e:'🐘',n:'elephant'},{e:'🌸',n:'flower'},{e:'🐶',n:'dog'},{e:'🌙',n:'moon'}],ok:'elephant'},
		{l:'F',w:[{e:'🌸',n:'flower'},{e:'🐱',n:'cat'},{e:'☀️',n:'sun'},{e:'🐴',n:'horse'}],ok:'flower'},
		{l:'G',w:[{e:'🐱',n:'cat'},{e:'🌙',n:'moon'},{e:'⭐',n:'star'},{e:'🐶',n:'dog'}],ok:'cat'},
		{l:'P',w:[{e:'🐶',n:'dog'},{e:'🏠',n:'house'},{e:'☀️',n:'sun'},{e:'🌸',n:'flower'}],ok:'dog'},
		{l:'M',w:[{e:'🦋',n:'butterfly'},{e:'🌙',n:'moon'},{e:'⭐',n:'star'},{e:'🐶',n:'dog'}],ok:'butterfly'},
		{l:'S',w:[{e:'☀️',n:'sun'},{e:'🐱',n:'cat'},{e:'🌸',n:'flower'},{e:'🐘',n:'elephant'}],ok:'sun'},
		{l:'T',w:[{e:'🐢',n:'turtle'},{e:'🌙',n:'moon'},{e:'🐶',n:'dog'},{e:'🌸',n:'flower'}],ok:'turtle'},
		{l:'L',w:[{e:'🦁',n:'lion'},{e:'⭐',n:'star'},{e:'🐶',n:'dog'},{e:'🏠',n:'house'}],ok:'lion'},
		{l:'R',w:[{e:'🐭',n:'mouse'},{e:'🐱',n:'cat'},{e:'🌸',n:'flower'},{e:'☀️',n:'sun'}],ok:'mouse'},
		{l:'N',w:[{e:'☁️',n:'cloud'},{e:'🏠',n:'house'},{e:'⭐',n:'star'},{e:'🐶',n:'dog'}],ok:'cloud'},
		{l:'H',w:[{e:'🐹',n:'hamster'},{e:'🐶',n:'dog'},{e:'🌸',n:'flower'},{e:'⭐',n:'star'}],ok:'hamster'},
		{l:'J',w:[{e:'🦒',n:'giraffe'},{e:'🌸',n:'flower'},{e:'🐶',n:'dog'},{e:'☀️',n:'sun'}],ok:'giraffe'},
		{l:'V',w:[{e:'🐮',n:'cow'},{e:'🐶',n:'dog'},{e:'🌙',n:'moon'},{e:'☀️',n:'sun'}],ok:'cow'},
		{l:'Z',w:[{e:'🥕',n:'carrot'},{e:'🌸',n:'flower'},{e:'🐶',n:'dog'},{e:'☀️',n:'sun'}],ok:'carrot'},
		{l:'Ñ',w:[{e:'🦤',n:'rhea'},{e:'🐶',n:'dog'},{e:'🌸',n:'flower'},{e:'☀️',n:'sun'}],ok:'rhea'},
	];

	/** @type {HTMLDivElement} */
	let container, g3Round = 0;
	/** @type {Array<{l:string,ok:string,w:Array<{n:string,e:string}>}>} */
	let g3Data = [];

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG3(cont, lv) {
		container = cont; g3Round = 0;
		const easy=['A','E','I','O','U','M','P','S','T','L'], med=['B','C','D','F','G','R','N'], hard=['J','V','Z','H','Ñ'];
		let pool;
		if(lv<=5) pool = G3_DATA.filter(d=>easy.includes(d.l));
		else if(lv<=10) pool = G3_DATA.filter(d=>[...easy,...med].includes(d.l));
		else pool = G3_DATA;
		g3Data = shuf(pool).slice(0, lerpParam(lv,5,8));
		window.ppSay(T('games.g3.hello'));
		g3Next();
	}

	function g3Next() {
		const lv = window.ppGetLevel();
		if(g3Round>=g3Data.length){const _lv=window.ppWin();window.ppCelebrate(T('games.g3.win'),3,()=>initG3(container,window.ppGetLevel()),_lv);return;}
		/** @type {HTMLElement} */ (container.querySelector('#g3pb')).style.width = (g3Round/g3Data.length*100)+'%';
		const d = g3Data[g3Round];
		const ltrEl = /** @type {HTMLElement} */ (container.querySelector('#g3ltr'));
		ltrEl.textContent = lv>=11?(d.l+' / '+d.l.toLowerCase()):d.l;
		const optsEl = /** @type {HTMLElement} */ (container.querySelector('#g3opts')); optsEl.innerHTML = '';
		const numOpts = lv<=5?Math.min(2+Math.floor((lv-1)/2),3):lv<=10?3:4;
		const shown = shuf(d.w).slice(0,numOpts);
		if(!shown.find(/** @param {{n:string}} w */ w=>w.n===d.ok)) shown[0] = /** @type {typeof shown[0]} */ (d.w.find(/** @param {{n:string}} w */ w=>w.n===d.ok));
		shuf(shown).forEach(w => {
			const b = document.createElement('div'); b.className = 'g3-opt';
			b.innerHTML = w.e+'<p>'+T('games.g3.words.'+w.n)+'</p>';
			b.onclick = () => {
				if(w.n===d.ok){b.style.background='#EFFFEF';b.style.borderColor='#6BCB77';window.ppBeep(880,.2);window.ppSay(T('games.g3.correct', {word: T('games.g3.words.'+d.ok), letter: d.l}));window.ppOnCorrect();g3Round++;setTimeout(g3Next,1100);}
				else{b.classList.add('err');setTimeout(()=>b.classList.remove('err'),400);window.ppOnWrong();window.ppBoo();window.ppSay(T('games.common.try_again'));}
			};
			optsEl.appendChild(b);
		});
		window.ppSay(T('games.g3.question', {letter: d.l}));
	}

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initContainer(cont, lv) {
		container = cont;
		cont.innerHTML = `
			<div class="pbar"><div class="pfill" id="g3pb" style="width:0%;background:var(--c3)"></div></div>
			<div class="ins">${T('games.g3.instruction')}</div>
			<div class="g3-letter" id="g3ltr">A</div>
			<div class="g3-opts" id="g3opts"></div>`;
		initG3(cont, lv);
	}
</script>

<GameShell gameNum={3} title="Letras" icon="🅰️" initGame={initContainer} />
