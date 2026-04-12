<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	const G23_DATA=[
		{f:'El gato bebe ___',a:'leche',x:['piedra','sol','libro']},
		{f:'El sol sale por la ___',a:'mañana',x:['mesa','silla','piedra']},
		{f:'Los pájaros tienen ___',a:'alas',x:['ruedas','patas','gafas']},
		{f:'En invierno hace mucho ___',a:'frío',x:['calor','verde','agua']},
		{f:'El perro mueve la ___',a:'cola',x:['mesa','rueda','nube']},
		{f:'Las flores crecen en el ___',a:'jardín',x:['cielo','mar','techo']},
		{f:'Los peces viven en el ___',a:'agua',x:['cielo','bosque','desierto']},
		{f:'Dormimos en la ___',a:'cama',x:['cocina','calle','nube']},
		{f:'Comemos con la ___',a:'boca',x:['oreja','pie','rodilla']},
		{f:'La lluvia cae del ___',a:'cielo',x:['suelo','mar','bosque']},
		{f:'Escribimos con un ___',a:'lápiz',x:['tenedor','zapato','vaso']},
		{f:'El avión vuela por el ___',a:'cielo',x:['mar','suelo','bosque']},
		{f:'Las estrellas salen de ___',a:'noche',x:['día','tarde','lunes']},
		{f:'Los bomberos apagan el ___',a:'fuego',x:['agua','viento','hielo']},
		{f:'El tren circula por las ___',a:'vías',x:['nubes','olas','hojas']},
	];

	function initG23(cont, lv) {
		let round = 0;
		const data = shuf(G23_DATA).slice(0, lerpParam(lv, 5, 8));

		cont.innerHTML = `<div class="ins">¡Completa la frase!</div>
			<div class="pbar"><div class="pfill" id="g23pb" style="width:0%;background:var(--c6)"></div></div>
			<div class="g23-frase" id="g23frase"></div>
			<div class="g8-opts" id="g23opts"></div>`;

		function next() {
			if (round >= data.length) { const _lv = window.ppWin(); window.ppCelebrate('¡Completas frases como un crack! 💬', 3, () => initG23(cont, window.ppGetLevel()), _lv); return; }
			cont.querySelector('#g23pb').style.width = (round/data.length*100)+'%';
			const d = data[round];
			cont.querySelector('#g23frase').textContent = d.f;
			const numOpts = lv<=3?2:lv<=7?3:4;
			const wrongs = d.x.slice(0, numOpts-1);
			const optsEl = cont.querySelector('#g23opts'); optsEl.innerHTML = '';
			shuf([d.a, ...wrongs]).forEach(c => {
				const b = document.createElement('div'); b.className = 'g8-opt'; b.textContent = c;
				b.onclick = () => {
					if(c===d.a){b.style.background='#EFFFEF';b.style.borderColor='#6BCB77';window.ppBeep(880,.2);window.ppSay('¡Correcto! '+d.f.replace('___',d.a));window.ppOnCorrect();round++;setTimeout(next,1200);}
					else{b.classList.add('err');setTimeout(()=>b.classList.remove('err'),400);window.ppOnWrong();window.ppBoo();window.ppSay('¡Inténtalo!');}
				};
				optsEl.appendChild(b);
			});
			window.ppSay(d.f.replace('___','¿qué?'));
		}
		next();
	}
</script>

<GameShell gameNum={23} title="Completa Frase" icon="💬" initGame={initG23} />
