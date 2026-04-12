<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	const G19_DATA=[
		{w:'Sol',s:1},{w:'Mar',s:1},{w:'Luz',s:1},{w:'Pan',s:1},
		{w:'Casa',s:2},{w:'Mesa',s:2},{w:'Luna',s:2},{w:'Gato',s:2},{w:'Perro',s:2},{w:'Bota',s:2},
		{w:'Pelota',s:3},{w:'Mariposa',s:4},{w:'Camisa',s:3},{w:'Zapato',s:3},{w:'Tomate',s:3},
		{w:'Elefante',s:4},{w:'Cocodrilo',s:4},{w:'Dinosaurio',s:4},{w:'Zanahoria',s:4},
		{w:'Helicóptero',s:5},{w:'Abecedario',s:5},{w:'Rinoceronte',s:5},
	];

	function initG19(cont, lv) {
		let round = 0;
		const maxSyl = lv<=3?2:lv<=6?3:lv<=9?4:5;
		const pool = G19_DATA.filter(d => d.s <= maxSyl);
		const data = shuf(pool).slice(0, lerpParam(lv, 5, 8));

		cont.innerHTML = `<div class="ins">¡Cuenta las sílabas dando palmadas!</div>
			<div class="pbar"><div class="pfill" id="g19pb" style="width:0%;background:var(--c1)"></div></div>
			<div class="g3-letter" id="g19word" style="font-size:3rem"></div>
			<div class="g2-nums" id="g19opts" style="display:flex"></div>`;

		function next() {
			if (round >= data.length) { const _lv = window.ppWin(); window.ppCelebrate('¡Silabeas genial! 👏', 3, () => initG19(cont, window.ppGetLevel()), _lv); return; }
			cont.querySelector('#g19pb').style.width = (round/data.length*100)+'%';
			const d = data[round];
			cont.querySelector('#g19word').textContent = d.w;
			const numOpts = lv<=5?2:lv<=10?3:4;
			const cols = ['#FF6B6B','#4D9FEC','#6BCB77','#FF9F43'];
			const vals = [d.s]; let tries=0;
			while(vals.length<numOpts&&tries<50){tries++;const r=Math.max(1,d.s+Math.floor(Math.random()*5)-2);if(!vals.includes(r)&&r>=1&&r<=6)vals.push(r);}
			const optsEl = cont.querySelector('#g19opts'); optsEl.innerHTML = '';
			shuf(vals).forEach((v,i) => {
				const b = document.createElement('button'); b.className = 'g2-num'; b.style.background = cols[i%4]; b.textContent = v;
				b.onclick = () => {
					if(v===d.s){b.style.background='#6BCB77';window.ppBeep(880,.2);window.ppSay('¡Correcto! '+d.w+' tiene '+d.s+(d.s===1?' sílaba':' sílabas'));window.ppOnCorrect();round++;setTimeout(next,1100);}
					else{b.classList.add('err');setTimeout(()=>b.classList.remove('err'),400);window.ppOnWrong();window.ppBoo();window.ppSay('¡Inténtalo!');}
				};
				optsEl.appendChild(b);
			});
			window.ppSay(d.w+'. ¿Cuántas sílabas tiene?');
		}
		next();
	}
</script>

<GameShell gameNum={19} title="Sílabas" icon="👏" initGame={initG19} />
