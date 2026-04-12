<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	const G16_SHAPES=['🔴','🔵','🟢','🟡','⭐','❤️','🌙','☀️','🐶','🐱','🌸','🌺','🔺','⭕','⬛','🟧'];

	function g16GenPattern(lv){
		const pool=shuf(G16_SHAPES);
		let seq,ans,opts;
		if(lv<=3){const a=pool[0],b=pool[1];seq=[a,b,a,b];ans=a;opts=[ans,...shuf(pool.filter(x=>x!==ans)).slice(0,1)];}
		else if(lv<=6){const a=pool[0],b=pool[1];seq=[a,b,a,b];ans=a;opts=[ans,...shuf(pool.filter(x=>x!==ans)).slice(0,2)];}
		else if(lv<=9){const a=pool[0],b=pool[1],c=pool[2];seq=[a,b,c,a,b];ans=c;opts=[ans,...shuf(pool.filter(x=>x!==ans)).slice(0,2)];}
		else if(lv<=12){const a=pool[0],b=pool[1];seq=[a,a,b,b,a,a];ans=b;opts=[ans,...shuf(pool.filter(x=>x!==ans)).slice(0,2)];}
		else{const a=pool[0],b=pool[1];seq=[a,b,a,b];ans=a;opts=[ans,...shuf(pool.filter(x=>x!==ans)).slice(0,3)];}
		return{seq,ans,opts};
	}

	function initG16(cont, lv) {
		let round=0;
		const total=lerpParam(lv,5,7);

		cont.innerHTML = `<div class="ins">¡Elige qué figura viene después!</div>
			<div class="pbar" id="g16pb"><div class="pbar-f"></div></div>
			<div class="g16-pattern" id="g16pattern"></div><div class="g16-opts" id="g16opts"></div>`;

		function setPbar(r,t){const f=cont.querySelector('#g16pb .pbar-f');if(f)f.style.width=(r/t*100)+'%';}

		function next(){
			if(round>=total){const _lv=window.ppWin();window.ppCelebrate('¡Eres maestro de patrones! 🔷',3,()=>initG16(cont,window.ppGetLevel()),_lv);return;}
			setPbar(round,total);
			const p=g16GenPattern(lv);
			const patEl=cont.querySelector('#g16pattern');patEl.innerHTML='';
			p.seq.forEach(s=>{const d=document.createElement('div');d.className='g16-item';d.textContent=s;patEl.appendChild(d);});
			const gap=document.createElement('div');gap.className='g16-gap';gap.textContent='?';patEl.appendChild(gap);
			const opEl=cont.querySelector('#g16opts');opEl.innerHTML='';
			const distractors=shuf(p.opts.filter(x=>x!==p.ans)).slice(0,lv<=3?1:lv<=6?2:3);
			const allOpts=shuf([p.ans,...distractors]);
			allOpts.forEach(o=>{
				const b=document.createElement('div');b.className='g16-opt';b.textContent=o;
				b.onclick=()=>{
					if(o===p.ans){b.style.borderColor='#6BCB77';b.style.background='#EFFFEF';
						gap.className='g16-item';gap.style.cssText='background:#EFFFEF;border:2px solid #6BCB77';gap.textContent=p.ans;
						window.ppBeep(880,.22);window.ppSay('¡Correcto!');window.ppOnCorrect();round++;setTimeout(next,1050);
					}else{b.classList.add('err');setTimeout(()=>b.classList.remove('err'),400);window.ppOnWrong();window.ppBoo();window.ppSay('¡Mira el patrón!');}
				};
				opEl.appendChild(b);
			});
			window.ppSay('¿Qué sigue después?');
		}
		window.ppSay('¡Mira la secuencia y elige qué figura viene después!');
		next();
	}
</script>

<GameShell gameNum={16} title="Patrones" icon="🔷" initGame={initG16} />
