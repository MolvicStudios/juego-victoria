<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { shuf, lerpParam } from '$lib/data.js';

	const G3_DATA=[
		{l:'A',w:[{e:'🌳',n:'Árbol'},{e:'✈️',n:'Avión'},{e:'🐝',n:'Abeja'},{e:'🌈',n:'Arco iris'}],ok:'Árbol'},
		{l:'B',w:[{e:'⛵',n:'Barco'},{e:'👢',n:'Bota'},{e:'⚽',n:'Balón'},{e:'🎈',n:'Globo'}],ok:'Barco'},
		{l:'C',w:[{e:'🏠',n:'Casa'},{e:'🚗',n:'Coche'},{e:'🐴',n:'Caballo'},{e:'🌙',n:'Luna'}],ok:'Casa'},
		{l:'D',w:[{e:'🐬',n:'Delfín'},{e:'🎲',n:'Dado'},{e:'🦕',n:'Dinosaurio'},{e:'⭐',n:'Estrella'}],ok:'Delfín'},
		{l:'E',w:[{e:'🐘',n:'Elefante'},{e:'⭐',n:'Estrella'},{e:'🪜',n:'Escalera'},{e:'🌸',n:'Flor'}],ok:'Elefante'},
		{l:'F',w:[{e:'🌸',n:'Flor'},{e:'🦭',n:'Foca'},{e:'🍓',n:'Fresa'},{e:'🐴',n:'Caballo'}],ok:'Flor'},
		{l:'G',w:[{e:'🐱',n:'Gato'},{e:'🎈',n:'Globo'},{e:'🦍',n:'Gorila'},{e:'🍪',n:'Galleta'}],ok:'Gato'},
		{l:'P',w:[{e:'🐶',n:'Perro'},{e:'🦆',n:'Pato'},{e:'🍕',n:'Pizza'},{e:'🏠',n:'Casa'}],ok:'Perro'},
		{l:'M',w:[{e:'🦋',n:'Mariposa'},{e:'🌙',n:'Luna'},{e:'🐒',n:'Mono'},{e:'🍎',n:'Manzana'}],ok:'Mariposa'},
		{l:'S',w:[{e:'☀️',n:'Sol'},{e:'🐍',n:'Serpiente'},{e:'🎨',n:'Arte'},{e:'🎵',n:'Música'}],ok:'Sol'},
		{l:'T',w:[{e:'🐢',n:'Tortuga'},{e:'🍅',n:'Tomate'},{e:'📺',n:'Televisión'},{e:'🌙',n:'Luna'}],ok:'Tortuga'},
		{l:'L',w:[{e:'🦁',n:'León'},{e:'📕',n:'Libro'},{e:'🍋',n:'Limón'},{e:'⭐',n:'Estrella'}],ok:'León'},
		{l:'R',w:[{e:'🐭',n:'Ratón'},{e:'⏰',n:'Reloj'},{e:'🌹',n:'Rosa'},{e:'🐱',n:'Gato'}],ok:'Ratón'},
		{l:'N',w:[{e:'☁️',n:'Nube'},{e:'🍊',n:'Naranja'},{e:'👃',n:'Nariz'},{e:'🏠',n:'Casa'}],ok:'Nube'},
		{l:'H',w:[{e:'🐹',n:'Hámster'},{e:'🍃',n:'Hoja'},{e:'🧊',n:'Hielo'},{e:'🐶',n:'Perro'}],ok:'Hámster'},
		{l:'J',w:[{e:'🦒',n:'Jirafa'},{e:'🎮',n:'Juego'},{e:'🧃',n:'Jugo'},{e:'🌸',n:'Flor'}],ok:'Jirafa'},
		{l:'V',w:[{e:'🐮',n:'Vaca'},{e:'🏐',n:'Voleibol'},{e:'🪟',n:'Ventana'},{e:'🐶',n:'Perro'}],ok:'Vaca'},
		{l:'Z',w:[{e:'🥕',n:'Zanahoria'},{e:'👟',n:'Zapato'},{e:'🦊',n:'Zorro'},{e:'🌸',n:'Flor'}],ok:'Zanahoria'},
		{l:'Ñ',w:[{e:'🎵',n:'Ñoño'},{e:'🦌',n:'Ñu'},{e:'🦊',n:'Zorro'},{e:'🐶',n:'Perro'}],ok:'Ñoño'},
	];

	let container, g3Round = 0, g3Data = [];

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
		container.querySelector('#g3pb').style.width = (g3Round/g3Data.length*100)+'%';
		const d = g3Data[g3Round];
		const ltrEl = container.querySelector('#g3ltr');
		ltrEl.textContent = lv>=11?(d.l+' / '+d.l.toLowerCase()):d.l;
		const optsEl = container.querySelector('#g3opts'); optsEl.innerHTML = '';
		const numOpts = lv<=5?Math.min(2+Math.floor((lv-1)/2),3):lv<=10?3:4;
		const shown = shuf(d.w).slice(0,numOpts);
		if(!shown.find(w=>w.n===d.ok)) shown[0] = d.w.find(w=>w.n===d.ok);
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
