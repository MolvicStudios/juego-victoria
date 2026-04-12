<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { shuf } from '$lib/data.js';

	const G9_SETS=[
		{p:['🌞','⭐','🌸','🦋','🐝','🌈','🌻','🍀','🌺'],t:'Jardín'},
		{p:['🐱','🐶','🐭','🐰','🐸','🦊','🐻','🐼','🐨'],t:'Animales'},
		{p:['🍎','🍊','🍋','🍇','🍓','🍑','🍒','🍌','🥝'],t:'Frutas'},
		{p:['🚗','✈️','⛵','🚀','🚂','🚌','🏍️','🚁','🛸'],t:'Vehículos'},
		{p:['🔺','⭕','⬛','🟧','💎','⭐','❤️','🌙','🔷'],t:'Formas'},
	];

	function initG9(cont, lv) {
		let sel=null,placed=0;
		const total=lv<=6?4:lv<=9?6:9;
		const colsN=lv<=6?2:3;
		const sz=lv<=6?95:lv<=9?80:70;
		const set=G9_SETS[Math.floor(Math.random()*G9_SETS.length)];
		const pieces=set.p.slice(0,total);

		cont.innerHTML = `<div class="ins">¡Toca una pieza y luego su lugar!</div>
			<div class="g9-grid" id="g9grid" style="grid-template-columns:repeat(${colsN},1fr)"></div>
			<div class="g9-tray" id="g9tray"></div>`;

		const gridEl=cont.querySelector('#g9grid'), trayEl=cont.querySelector('#g9tray');
		const showHint=lv<=3, flashHint=lv>=13;

		for(let i=0;i<total;i++){
			const s=document.createElement('div');s.className='g9-slot';s.dataset.p=i;s.dataset.v=pieces[i];
			s.style.cssText=`width:${sz}px;height:${sz}px`;
			if(showHint){s.textContent=pieces[i];s.style.opacity='.15';}
			if(flashHint){s.textContent=pieces[i];s.style.opacity='.2';}
			s.onclick=()=>place(i);
			gridEl.appendChild(s);
		}
		if(flashHint){
			setTimeout(()=>gridEl.querySelectorAll('.g9-slot').forEach(s=>{if(!s.classList.contains('filled')){s.textContent='';s.style.opacity='';}}),1000);
		}

		shuf(pieces.map((p,i)=>({p,i}))).forEach(({p})=>{
			const d=document.createElement('div');d.className='g9-piece';d.dataset.v=p;
			d.style.cssText=`width:${sz}px;height:${sz}px;font-size:${sz*.55}px`;
			d.textContent=p;d.onclick=()=>selPiece(d);
			trayEl.appendChild(d);
		});

		function selPiece(el){
			if(el.classList.contains('used'))return;sel=el;
			cont.querySelectorAll('.g9-piece').forEach(x=>x.classList.remove('sel'));
			el.classList.add('sel');window.ppBeep(600,.1);
		}

		function place(i){
			if(!sel){window.ppSay('Primero toca una pieza');return;}
			const sl=gridEl.children[i];if(sl.classList.contains('filled'))return;
			if(sl.dataset.v===sel.dataset.v){
				sl.textContent=sel.dataset.v;sl.classList.add('filled');sl.style.opacity='';
				sl.style.fontSize=sl.style.height.replace('px','')*0.55+'px';
				sel.classList.add('used');sel.classList.remove('sel');sel=null;
				window.ppBeep(700,.15);window.ppOnCorrect();placed++;
				if(placed===total){const _lv=window.ppWin();setTimeout(()=>window.ppCelebrate('¡Puzle completo! 🧩',3,()=>initG9(cont,window.ppGetLevel()),_lv),300);}
			}else{
				sl.classList.add('err');setTimeout(()=>sl.classList.remove('err'),400);
				window.ppOnWrong();window.ppBoo();window.ppSay('¡Ese no va ahí!');
			}
		}
		window.ppSay('¡Toca una pieza y luego su lugar en el cuadro!');
	}
</script>

<GameShell gameNum={9} title="Mini Puzle" icon="🧩" initGame={initG9} />
