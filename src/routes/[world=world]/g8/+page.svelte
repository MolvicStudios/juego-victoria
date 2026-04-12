<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	const G8_DATA=[
		{e:'🦁',w:'León',x:['Tigre','Oso','Lobo']},{e:'🐘',w:'Elefante',x:['Jirafa','Hipopótamo','Rinoceronte']},
		{e:'🍎',w:'Manzana',x:['Pera','Naranja','Cereza']},{e:'🚀',w:'Cohete',x:['Avión','Globo','Helicóptero']},
		{e:'🌈',w:'Arco iris',x:['Nube','Tormenta','Lluvia']},{e:'🐬',w:'Delfín',x:['Ballena','Tiburón','Pez']},
		{e:'🍕',w:'Pizza',x:['Hamburguesa','Pasta','Sándwich']},{e:'🦋',w:'Mariposa',x:['Abeja','Libélula','Mosca']},
		{e:'🏠',w:'Casa',x:['Castillo','Edificio','Cabaña']},{e:'🌸',w:'Flor',x:['Árbol','Hierba','Cactus']},
		{e:'🚂',w:'Tren',x:['Coche','Barco','Bicicleta']},{e:'🍦',w:'Helado',x:['Pastel','Galleta','Chocolate']},
		{e:'🐢',w:'Tortuga',x:['Caracol','Rana','Lagarto']},{e:'⭐',w:'Estrella',x:['Luna','Sol','Planeta']},
		{e:'🎸',w:'Guitarra',x:['Piano','Tambor','Flauta']},
	];

	function initG8(cont, lv) {
		let round = 0;
		const data = shuf(G8_DATA).slice(0, lerpParam(lv,5,8));

		cont.innerHTML = `<div class="ins">¡Mira el dibujo y elige cómo se llama!</div>
			<div class="pbar" id="g8pb"><div class="pfill"></div></div>
			<div class="g8-emo" id="g8emo"></div><div class="g8-opts" id="g8opts"></div>`;

		function setPbar(r,t){const f=cont.querySelector('#g8pb .pfill');if(f)f.style.width=(r/t*100)+'%';}

		function next() {
			if(round>=data.length){const _lv=window.ppWin();window.ppCelebrate('¡Sabes muchísimas palabras! 📚',3,()=>initG8(cont,window.ppGetLevel()),_lv);return;}
			setPbar(round,data.length);
			const d=data[round];
			const audioOnly=lv>=12;
			const ee=cont.querySelector('#g8emo');ee.textContent=d.e;ee.style.animation='none';void ee.offsetWidth;ee.style.animation='popIn .35s';
			ee.style.visibility=audioOnly?'hidden':'';

			const numWrong=lv<=3?1:lv<=7?2:3;
			const wrongs=d.x.slice(0,numWrong);
			const optsEl=cont.querySelector('#g8opts');optsEl.innerHTML='';
			shuf([d.w,...wrongs]).forEach(c=>{
				const b=document.createElement('div');b.className='g8-opt';b.textContent=c;
				b.onclick=()=>{
					if(c===d.w){b.style.background='#EFFFEF';b.style.borderColor='#6BCB77';
						window.ppBeep(880,.2);window.ppSay('¡Correcto! ¡'+d.w+'!');window.ppOnCorrect();round++;setTimeout(next,900);
					}else{b.classList.add('err');setTimeout(()=>b.classList.remove('err'),400);window.ppOnWrong();window.ppBoo();window.ppSay('¡Inténtalo!');}
				};
				optsEl.appendChild(b);
			});
			if(audioOnly){window.ppSay('Escucha con atención');setTimeout(()=>window.ppSay(d.w),600);}else{window.ppSay('¿Cómo se llama esto?');}
		}
		window.ppSay('¡Mira el dibujo y elige cómo se llama!');
		next();
	}
</script>

<GameShell gameNum={8} title="¿Qué Ves?" icon="👀" initGame={initG8} />
