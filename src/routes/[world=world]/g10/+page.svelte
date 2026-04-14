<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { shuf } from '$lib/data.js';

	/** @type {(key: string, vars?: Record<string, string|number>) => string} */ const T = (key, vars) => window.ppT?.(key, vars) ?? key;

	const G10_COLS=[
		{key:'red',h:'#E53E3E'},{key:'blue',h:'#4299E1'},{key:'green',h:'#48BB78'},{key:'yellow',h:'#ECC94B'},
		{key:'orange',h:'#ED8936'},{key:'purple',h:'#9F7AEA'},{key:'pink',h:'#ED64A6'},{key:'brown',h:'#975A16'},
	];
	const G10_MIX=[{key:'red_blue',a:'purple'},{key:'red_yellow',a:'orange'},{key:'blue_yellow',a:'green'}];

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG10(cont, lv) {
		let round=0;
		const numCols=lv<=4?4:lv<=7?6:8;
		/** @type {({key:string,h:string}|{isMix:boolean,key:string,a:string})[]} */
		let order=shuf(G10_COLS.slice(0,numCols));
		if(lv>=14){
			const mix=shuf(G10_MIX).slice(0,2).map(m=>({...m,isMix:/** @type {true} */(true)}));
			order=[...order,...mix];order=shuf(order);
		}

		cont.innerHTML = `<div class="ins">${T('games.g10.instruction')}</div>
			<div class="pbar" id="g10pb"><div class="pfill" style="background:var(--c2)"></div></div>
			<div class="g10-name" id="g10name"></div><div class="g10-circles" id="g10circles"></div>`;

		/** @param {number} r @param {number} t */
		function setPbar(r,t){const f=/** @type {HTMLElement} */ (cont.querySelector('#g10pb .pfill'));f.style.width=(r/t*100)+'%';}

		function next(){
			if(round>=order.length){const _lv=window.ppWin();window.ppCelebrate(T('games.g10.win')+' 🌈',3,()=>initG10(cont,window.ppGetLevel()),_lv);return;}
			setPbar(round,order.length);
			const t=order[round];
			const nm=/** @type {HTMLElement} */ (cont.querySelector('#g10name'));
			const audioOnly=lv>=11&&lv<14;
			const circlesEl=/** @type {HTMLElement} */ (cont.querySelector('#g10circles'));

			if('isMix' in t){
				nm.textContent=T('games.g10.mix.'+t.key);nm.style.color='var(--ink)';
				const answer=G10_COLS.find(c=>c.key===t.a);
				if(!answer) return;
				const others=G10_COLS.filter(c=>c.key!==t.a);
				const shown=shuf([answer,...shuf(others).slice(0,4)]);
				circlesEl.innerHTML='';
				shown.forEach(c=>{
					const d=document.createElement('div');d.className='g10-c';
					d.style.background=c.h;d.style.boxShadow='0 5px 0 '+c.h+'88';
					d.onclick=()=>{
						if(c.key===t.a){window.ppBeep(880,.2);window.ppSay(T('games.g10.correct_name',{name:T('games.g10.colors.'+t.a)}));window.ppOnCorrect();round++;setTimeout(next,800);}
						else{d.classList.add('err');setTimeout(()=>d.classList.remove('err'),400);window.ppOnWrong();window.ppBoo();}
					};
					circlesEl.appendChild(d);
				});
				window.ppSay(T('games.g10.what_color'));
			}else{
				if(audioOnly){nm.textContent='🔊';nm.style.color='var(--ink)';}
				else{nm.textContent=T('games.g10.colors.'+t.key);nm.style.color=t.h;}
				const others=G10_COLS.filter(c=>c.h!==t.h);
				const shown=shuf([t,...shuf(others).slice(0,5)]);
				circlesEl.innerHTML='';
				shown.forEach(c=>{
					const d=document.createElement('div');d.className='g10-c';
					d.style.background=c.h;d.style.boxShadow='0 5px 0 '+c.h+'88';
					d.onclick=()=>{
						if(c.h===t.h){window.ppBeep(880,.2);window.ppSay(T('games.g10.correct_name',{name:T('games.g10.colors.'+t.key)}));window.ppOnCorrect();round++;setTimeout(next,800);}
						else{d.classList.add('err');setTimeout(()=>d.classList.remove('err'),400);window.ppOnWrong();window.ppBoo();window.ppSay(T('games.g10.find',{name:T('games.g10.colors.'+t.key)}));}
					};
					circlesEl.appendChild(d);
				});
				window.ppSay(T('games.g10.touch',{name:T('games.g10.colors.'+t.key)}));
			}
		}
		window.ppSay(T('games.g10.hello'));
		next();
	}
</script>

<GameShell gameNum={10} title="Colores" icon="🌈" initGame={initG10} />
