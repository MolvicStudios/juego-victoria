<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { shuf, lerpParam } from '$lib/data.js';

	const G3_DATA=[
		{l:'A',w:[{e:'🌳',n:'Árbol'},{e:'🌸',n:'Flor'},{e:'🐶',n:'Perro'},{e:'🌙',n:'Luna'}],ok:'Árbol'},
		{l:'B',w:[{e:'⛵',n:'Barco'},{e:'☀️',n:'Sol'},{e:'🐘',n:'Elefante'},{e:'🌈',n:'Arco iris'}],ok:'Barco'},
		{l:'C',w:[{e:'🏠',n:'Casa'},{e:'🌙',n:'Luna'},{e:'🐶',n:'Perro'},{e:'🌸',n:'Flor'}],ok:'Casa'},
		{l:'D',w:[{e:'🐬',n:'Delfín'},{e:'⭐',n:'Estrella'},{e:'🌸',n:'Flor'},{e:'🐱',n:'Gato'}],ok:'Delfín'},
		{l:'E',w:[{e:'🐘',n:'Elefante'},{e:'🌸',n:'Flor'},{e:'🐶',n:'Perro'},{e:'🌙',n:'Luna'}],ok:'Elefante'},
		{l:'F',w:[{e:'🌸',n:'Flor'},{e:'🐱',n:'Gato'},{e:'☀️',n:'Sol'},{e:'🐴',n:'Caballo'}],ok:'Flor'},
		{l:'G',w:[{e:'🐱',n:'Gato'},{e:'🌙',n:'Luna'},{e:'⭐',n:'Estrella'},{e:'🐶',n:'Perro'}],ok:'Gato'},
		{l:'P',w:[{e:'🐶',n:'Perro'},{e:'🏠',n:'Casa'},{e:'☀️',n:'Sol'},{e:'🌸',n:'Flor'}],ok:'Perro'},
		{l:'M',w:[{e:'🦋',n:'Mariposa'},{e:'🌙',n:'Luna'},{e:'⭐',n:'Estrella'},{e:'🐶',n:'Perro'}],ok:'Mariposa'},
		{l:'S',w:[{e:'☀️',n:'Sol'},{e:'🐱',n:'Gato'},{e:'🌸',n:'Flor'},{e:'🐘',n:'Elefante'}],ok:'Sol'},
		{l:'T',w:[{e:'🐢',n:'Tortuga'},{e:'🌙',n:'Luna'},{e:'🐶',n:'Perro'},{e:'🌸',n:'Flor'}],ok:'Tortuga'},
		{l:'L',w:[{e:'🦁',n:'León'},{e:'⭐',n:'Estrella'},{e:'🐶',n:'Perro'},{e:'🏠',n:'Casa'}],ok:'León'},
		{l:'R',w:[{e:'🐭',n:'Ratón'},{e:'🐱',n:'Gato'},{e:'🌸',n:'Flor'},{e:'☀️',n:'Sol'}],ok:'Ratón'},
		{l:'N',w:[{e:'☁️',n:'Nube'},{e:'🏠',n:'Casa'},{e:'⭐',n:'Estrella'},{e:'🐶',n:'Perro'}],ok:'Nube'},
		{l:'H',w:[{e:'🐹',n:'Hámster'},{e:'🐶',n:'Perro'},{e:'🌸',n:'Flor'},{e:'⭐',n:'Estrella'}],ok:'Hámster'},
		{l:'J',w:[{e:'🦒',n:'Jirafa'},{e:'🌸',n:'Flor'},{e:'🐶',n:'Perro'},{e:'☀️',n:'Sol'}],ok:'Jirafa'},
		{l:'V',w:[{e:'🐮',n:'Vaca'},{e:'🐶',n:'Perro'},{e:'🌙',n:'Luna'},{e:'☀️',n:'Sol'}],ok:'Vaca'},
		{l:'Z',w:[{e:'🥕',n:'Zanahoria'},{e:'🌸',n:'Flor'},{e:'🐶',n:'Perro'},{e:'☀️',n:'Sol'}],ok:'Zanahoria'},
		{l:'Ñ',w:[{e:'🦤',n:'Ñandú'},{e:'🐶',n:'Perro'},{e:'🌸',n:'Flor'},{e:'☀️',n:'Sol'}],ok:'Ñandú'},
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
		window.ppSay('¡Mira la letra y elige la imagen que empieza igual!');
		g3Next();
	}

	function g3Next() {
		const lv = window.ppGetLevel();
		if(g3Round>=g3Data.length){const _lv=window.ppWin();window.ppCelebrate('¡Conoces todas las letras! 🅰️',3,()=>initG3(container,window.ppGetLevel()),_lv);return;}
		/** @type {HTMLElement} */ (container.querySelector('#g3pb')).style.width = (g3Round/g3Data.length*100)+'%';
		const d = g3Data[g3Round];
		const ltrEl = /** @type {HTMLElement} */ (container.querySelector('#g3ltr'));
		ltrEl.textContent = lv>=11?(d.l+' / '+d.l.toLowerCase()):d.l;
		const optsEl = /** @type {HTMLElement} */ (container.querySelector('#g3opts')); optsEl.innerHTML = '';
		const numOpts = lv<=5?Math.min(2+Math.floor((lv-1)/2),3):lv<=10?3:4;
		const shown = shuf(d.w).slice(0,numOpts);
		if(!shown.find(/** @param {{n:string}} w */ w=>w.n===d.ok)) shown[0] = d.w.find(/** @param {{n:string}} w */ w=>w.n===d.ok);
		shuf(shown).forEach(w => {
			const b = document.createElement('div'); b.className = 'g3-opt';
			b.innerHTML = w.e+'<p>'+w.n+'</p>';
			b.onclick = () => {
				if(w.n===d.ok){b.style.background='#EFFFEF';b.style.borderColor='#6BCB77';window.ppBeep(880,.2);window.ppSay('¡Correcto! '+d.ok+' empieza por '+d.l);window.ppOnCorrect();g3Round++;setTimeout(g3Next,1100);}
				else{b.classList.add('err');setTimeout(()=>b.classList.remove('err'),400);window.ppOnWrong();window.ppBoo();window.ppSay('¡Inténtalo!');}
			};
			optsEl.appendChild(b);
		});
		window.ppSay('¿Qué empieza por '+d.l+'?');
	}

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initContainer(cont, lv) {
		container = cont;
		cont.innerHTML = `
			<div class="pbar"><div class="pfill" id="g3pb" style="width:0%;background:var(--c3)"></div></div>
			<div class="ins">¿Qué imagen empieza por esta letra?</div>
			<div class="g3-letter" id="g3ltr">A</div>
			<div class="g3-opts" id="g3opts"></div>`;
		initG3(cont, lv);
	}
</script>

<GameShell gameNum={3} title="Letras" icon="🅰️" initGame={initContainer} />
