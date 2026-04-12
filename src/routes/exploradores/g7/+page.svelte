<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	const G7_COLS=['#FF6B6B','#FF9F43','#FFD93D','#6BCB77','#4D9FEC','#A78BFA','#F472B6','#2DD4BF','#FF6B6B','#4D9FEC'];

	function initG7(cont, lv) {
		const max = lv<=3?lerpParam(lv,3,3):lv<=6?lerpParam(lv-3,4,5):lv<=9?lerpParam(lv-6,5,7):10;
		const reverse = lv>=13;
		let next = reverse?max:1;

		cont.innerHTML = `<div class="ins" id="g7ins">${reverse?'Del '+max+' al 1 ¡al revés!':'Del 1 al '+max+' en orden'}</div>
			<div class="g7-track" id="g7track"></div><div class="g7-pool" id="g7pool"></div>`;

		const track = cont.querySelector('#g7track'), pool = cont.querySelector('#g7pool');
		for(let i=1;i<=max;i++){
			const s=document.createElement('div');s.className='g7-slot';s.id='g7s'+i;
			s.textContent=reverse?(max-i+1):i;
			track.appendChild(s);
		}
		shuf(Array.from({length:max},(_,i)=>i+1)).forEach(n=>{
			const b=document.createElement('button');b.className='g7-ball';b.id='g7b'+n;
			b.style.background=G7_COLS[(n-1)%G7_COLS.length];b.textContent=n;
			b.onclick=()=>{
				if(n===next){
					const idx=reverse?(max-n+1):n;
					const sl=cont.querySelector('#g7s'+idx);sl.classList.add('ok');sl.style.background=G7_COLS[(n-1)%G7_COLS.length];sl.style.borderColor=G7_COLS[(n-1)%G7_COLS.length];
					b.classList.add('bye');window.ppBeep(300+n*60,.15);window.ppSay(n+'');window.ppOnCorrect();
					next+=reverse?-1:1;
					const done=reverse?(next<1):(next>max);
					if(done){const _lv=window.ppWin();setTimeout(()=>window.ppCelebrate(reverse?'¡Al revés perfecto! 🔢':'¡Contaste hasta '+max+'! 🔢',3,()=>initG7(cont,window.ppGetLevel()),_lv),500);}
				}else{b.classList.add('err');setTimeout(()=>b.classList.remove('err'),400);window.ppOnWrong();window.ppBoo();
					window.ppSay('¡El '+next+' primero!');}
			};
			pool.appendChild(b);
		});
		window.ppSay('¡Toca los números en orden!');
	}
</script>

<GameShell gameNum={7} title="Números en Orden" icon="🔢" initGame={initG7} />
