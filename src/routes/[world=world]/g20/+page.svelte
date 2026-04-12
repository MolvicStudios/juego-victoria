<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	const G20_DATA=[
		{w:'Gato',r:'Pato',x:['Perro','Casa','Sol']},
		{w:'Luna',r:'Cuna',x:['Nube','Gato','Mesa']},
		{w:'Ratón',r:'Balón',x:['Casa','Perro','Luna']},
		{w:'Flor',r:'Color',x:['Mesa','Gato','Nube']},
		{w:'Estrella',r:'Botella',x:['Mesa','Gato','Luna']},
		{w:'Camión',r:'Avión',x:['Casa','Perro','Mesa']},
		{w:'Zapato',r:'Plato',x:['Luna','Sol','Nube']},
		{w:'Canción',r:'Corazón',x:['Mesa','Perro','Casa']},
		{w:'Campana',r:'Manzana',x:['Gato','Sol','Perro']},
		{w:'Silla',r:'Ardilla',x:['Luna','Mesa','Casa']},
		{w:'Conejo',r:'Espejo',x:['Gato','Sol','Nube']},
		{w:'Tortuga',r:'Lechuga',x:['Perro','Luna','Mesa']},
		{w:'Coche',r:'Noche',x:['Gato','Casa','Sol']},
		{w:'Piso',r:'Aviso',x:['Luna','Perro','Mesa']},
		{w:'Ballena',r:'Arena',x:['Gato','Sol','Casa']},
	];

	function initG20(cont, lv) {
		let round = 0;
		const data = shuf(G20_DATA).slice(0, lerpParam(lv, 5, 8));

		cont.innerHTML = `<div class="ins">¡Encuentra la palabra que rima!</div>
			<div class="pbar"><div class="pfill" id="g20pb" style="width:0%;background:var(--c5)"></div></div>
			<div class="g3-letter" id="g20word" style="font-size:2.8rem"></div>
			<div class="g8-opts" id="g20opts"></div>`;

		function next() {
			if (round >= data.length) { const _lv = window.ppWin(); window.ppCelebrate('¡Eres un poeta! 🎤', 3, () => initG20(cont, window.ppGetLevel()), _lv); return; }
			cont.querySelector('#g20pb').style.width = (round/data.length*100)+'%';
			const d = data[round];
			cont.querySelector('#g20word').textContent = '🎤 ' + d.w;
			const numWrong = lv<=3?1:lv<=7?2:3;
			const wrongs = d.x.slice(0, numWrong);
			const optsEl = cont.querySelector('#g20opts'); optsEl.innerHTML = '';
			shuf([d.r, ...wrongs]).forEach(c => {
				const b = document.createElement('div'); b.className = 'g8-opt'; b.textContent = c;
				b.onclick = () => {
					if(c===d.r){b.style.background='#EFFFEF';b.style.borderColor='#6BCB77';window.ppBeep(880,.2);window.ppSay('¡Correcto! '+d.w+' rima con '+d.r);window.ppOnCorrect();round++;setTimeout(next,1100);}
					else{b.classList.add('err');setTimeout(()=>b.classList.remove('err'),400);window.ppOnWrong();window.ppBoo();window.ppSay('¡Inténtalo!');}
				};
				optsEl.appendChild(b);
			});
			window.ppSay('¿Qué rima con '+d.w+'?');
		}
		next();
	}
</script>

<GameShell gameNum={20} title="Rimas" icon="🎤" initGame={initG20} />
