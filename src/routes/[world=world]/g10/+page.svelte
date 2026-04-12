<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { shuf } from '$lib/data.js';

	const G10_COLS=[
		{n:'ROJO',h:'#E53E3E'},{n:'AZUL',h:'#4299E1'},{n:'VERDE',h:'#48BB78'},{n:'AMARILLO',h:'#ECC94B'},
		{n:'NARANJA',h:'#ED8936'},{n:'MORADO',h:'#9F7AEA'},{n:'ROSA',h:'#ED64A6'},{n:'MARRÓN',h:'#975A16'},
	];
	const G10_MIX=[{q:'Rojo + Azul = ?',a:'MORADO'},{q:'Rojo + Amarillo = ?',a:'NARANJA'},{q:'Azul + Amarillo = ?',a:'VERDE'}];

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG10(cont, lv) {
		let round=0;
		const numCols=lv<=4?4:lv<=7?6:8;
		/** @type {({n:string,h:string}|{isMix:boolean,q:string,a:string})[]} */
		let order=shuf(G10_COLS.slice(0,numCols));
		if(lv>=14){
			const mix=shuf(G10_MIX).slice(0,2).map(m=>({...m,isMix:/** @type {true} */(true)}));
			order=[...order,...mix];order=shuf(order);
		}

		cont.innerHTML = `<div class="ins">¡Toca el círculo del color!</div>
			<div class="pbar" id="g10pb"><div class="pfill" style="background:var(--c2)"></div></div>
			<div class="g10-name" id="g10name"></div><div class="g10-circles" id="g10circles"></div>`;

		/** @param {number} r @param {number} t */
		function setPbar(r,t){const f=/** @type {HTMLElement} */ (cont.querySelector('#g10pb .pfill'));f.style.width=(r/t*100)+'%';}

		function next(){
			if(round>=order.length){const _lv=window.ppWin();window.ppCelebrate('¡Conoces todos los colores! 🌈',3,()=>initG10(cont,window.ppGetLevel()),_lv);return;}
			setPbar(round,order.length);
			const t=order[round];
			const nm=/** @type {HTMLElement} */ (cont.querySelector('#g10name'));
			const audioOnly=lv>=11&&lv<14;
			const circlesEl=/** @type {HTMLElement} */ (cont.querySelector('#g10circles'));

			if('isMix' in t){
				nm.textContent=t.q;nm.style.color='var(--ink)';
				const answer=G10_COLS.find(c=>c.n===t.a);
				if(!answer) return;
				const others=G10_COLS.filter(c=>c.n!==t.a);
				const shown=shuf([answer,...shuf(others).slice(0,4)]);
				circlesEl.innerHTML='';
				shown.forEach(c=>{
					const d=document.createElement('div');d.className='g10-c';
					d.style.background=c.h;d.style.boxShadow='0 5px 0 '+c.h+'88';
					d.onclick=()=>{
						if(c.n===t.a){window.ppBeep(880,.2);window.ppSay('¡Correcto! ¡'+t.a+'!');window.ppOnCorrect();round++;setTimeout(next,800);}
						else{d.classList.add('err');setTimeout(()=>d.classList.remove('err'),400);window.ppOnWrong();window.ppBoo();}
					};
					circlesEl.appendChild(d);
				});
				window.ppSay('¿Qué color sale?');
			}else{
				if(audioOnly){nm.textContent='🔊';nm.style.color='var(--ink)';}
				else{nm.textContent=t.n;nm.style.color=t.h;}
				const others=G10_COLS.filter(c=>c.h!==t.h);
				const shown=shuf([t,...shuf(others).slice(0,5)]);
				circlesEl.innerHTML='';
				shown.forEach(c=>{
					const d=document.createElement('div');d.className='g10-c';
					d.style.background=c.h;d.style.boxShadow='0 5px 0 '+c.h+'88';
					d.onclick=()=>{
						if(c.h===t.h){window.ppBeep(880,.2);window.ppSay('¡Correcto! ¡'+t.n+'!');window.ppOnCorrect();round++;setTimeout(next,800);}
						else{d.classList.add('err');setTimeout(()=>d.classList.remove('err'),400);window.ppOnWrong();window.ppBoo();window.ppSay('¡Busca el '+t.n+'!');}
					};
					circlesEl.appendChild(d);
				});
				window.ppSay('Toca el color '+t.n);
			}
		}
		window.ppSay('¡Toca el círculo del color que te pido!');
		next();
	}
</script>

<GameShell gameNum={10} title="Colores" icon="🌈" initGame={initG10} />
