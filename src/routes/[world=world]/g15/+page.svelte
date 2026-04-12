<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	const G15_SETS=[
		{items:[{e:'🐘',n:'Elefante'},{e:'�',n:'Perro'},{e:'🐭',n:'Ratón'},{e:'🐜',n:'Hormiga'}]},
		{items:[{e:'🌳',n:'Árbol'},{e:'🌻',n:'Girasol'},{e:'🌸',n:'Flor'},{e:'🌱',n:'Semilla'}]},
		{items:[{e:'🚌',n:'Autobús'},{e:'🚗',n:'Coche'},{e:'🛵',n:'Moto'},{e:'🛴',n:'Patinete'}]},
		{items:[{e:'🏔️',n:'Montaña'},{e:'🏠',n:'Casa'},{e:'⛺',n:'Tienda'},{e:'📦',n:'Caja'}]},
		{items:[{e:'🐋',n:'Ballena'},{e:'🐬',n:'Delfín'},{e:'🐟',n:'Pez'},{e:'🦐',n:'Gamba'}]},
		{items:[{e:'🚀',n:'Cohete'},{e:'✈️',n:'Avión'},{e:'🦋',n:'Mariposa'},{e:'🐝',n:'Abeja'}]},
		{items:[{e:'🌞',n:'Sol'},{e:'🌙',n:'Luna'},{e:'⭐',n:'Estrellita'},{e:'✨',n:'Chispa'}]},
		{items:[{e:'🏰',n:'Castillo'},{e:'🏠',n:'Casita'},{e:'🎩',n:'Sombrero'},{e:'🧢',n:'Gorra'}]},
		{items:[{e:'🦕',n:'Dinosaurio'},{e:'🐊',n:'Cocodrilo'},{e:'🦎',n:'Lagarto'},{e:'🐛',n:'Gusano'}]},
		{items:[{e:'🎪',n:'Circo'},{e:'🎡',n:'Noria'},{e:'🎠',n:'Tiovivo'},{e:'🪁',n:'Cometa'}]},
	];
	const G15_SIZES=['5.4rem','3rem','1.7rem','1rem'];

	function initG15(cont, lv) {
		let round=0;
		const total=lerpParam(lv,5,7);

		cont.innerHTML = `<div class="ins" id="g15ins"></div>
			<div class="pbar" id="g15pb"><div class="pfill"></div></div>
			<div class="g15-objects" id="g15objects"></div>`;

		function setPbar(r,t){const f=cont.querySelector('#g15pb .pfill');if(f)f.style.width=(r/t*100)+'%';}

		function next(){
			if(round>=total){const _lv=window.ppWin();window.ppCelebrate('¡Sabes los tamaños! 📏',3,()=>initG15(cont,window.ppGetLevel()),_lv);return;}
			setPbar(round,total);
			const numItems=lv<=6?2:lv<=12?3:4;
			const set=G15_SETS[Math.floor(Math.random()*G15_SETS.length)];
			const items=set.items.slice(0,Math.min(numItems,set.items.length));
			let askType,correctName,qTxt;

			if(lv<=3){askType='big';correctName=items[0].n;qTxt='¿Cuál es más GRANDE? 👆';}
			else if(lv<=6){askType=Math.random()>.5?'big':'small';correctName=askType==='big'?items[0].n:items[items.length-1].n;qTxt=askType==='big'?'¿Cuál es más GRANDE? 👆':'¿Cuál es más PEQUEÑO? 👇';}
			else if(lv<=9){askType=Math.random()>.5?'big':'small';correctName=askType==='big'?items[0].n:items[items.length-1].n;qTxt=askType==='big'?'¿Cuál es más GRANDE? 👆':'¿Cuál es más PEQUEÑO? 👇';}
			else if(lv<=12){askType='medium';correctName=items[1].n;qTxt='¿Cuál es el MEDIANO? 🤔';}
			else{askType='order';qTxt='¡Toca del más grande al más pequeño!';}

			const qEl=cont.querySelector('#g15ins');qEl.textContent=qTxt;
			qEl.style.color=askType==='big'?'var(--c1)':askType==='small'?'var(--c5)':'var(--c6)';
			window.ppSay(qTxt.replace(/[👆👇🤔]/g,''));

			const vEl=cont.querySelector('#g15objects');vEl.innerHTML='';

			if(askType==='order'){
				let orderIdx=0;
				const displayed=shuf(items.map((it,i)=>({...it,sizeIdx:i})));
				displayed.forEach(it=>{
					const d=document.createElement('div');d.className='g15-obj';
					const emo=document.createElement('span');emo.className='g15-emo';emo.style.fontSize=G15_SIZES[it.sizeIdx];emo.textContent=it.e;
					const lbl=document.createElement('span');lbl.className='g15-lbl';lbl.textContent=it.n;
					d.appendChild(emo);d.appendChild(lbl);
					d.onclick=()=>{
						if(it.sizeIdx===orderIdx){d.classList.add('hit-ok');d.style.pointerEvents='none';window.ppBeep(880,.15);orderIdx++;
							if(orderIdx>=items.length){window.ppOnCorrect();round++;setTimeout(next,700);}
						}else{d.classList.add('hit-err');setTimeout(()=>d.classList.remove('hit-err'),400);window.ppOnWrong();window.ppBoo();window.ppSay('¡Busca el más grande primero!');}
					};
					vEl.appendChild(d);
				});
			}else{
				const displayed=shuf(items.map((it,i)=>({...it,sizeIdx:i})));
				displayed.forEach(it=>{
					const d=document.createElement('div');d.className='g15-obj';
					const emo=document.createElement('span');emo.className='g15-emo';emo.style.fontSize=G15_SIZES[it.sizeIdx];emo.textContent=it.e;
					const lbl=document.createElement('span');lbl.className='g15-lbl';if(lv>=3)lbl.textContent=it.n;
					d.appendChild(emo);d.appendChild(lbl);
					d.onclick=()=>{
						if(it.n===correctName){d.classList.add('hit-ok');window.ppBeep(880,.22);window.ppSay('¡Correcto! ¡'+it.n+'!');window.ppOnCorrect();round++;setTimeout(next,950);}
						else{d.classList.add('hit-err');setTimeout(()=>d.classList.remove('hit-err'),400);window.ppOnWrong();window.ppBoo();window.ppSay('¡Mira bien el tamaño!');}
					};
					vEl.appendChild(d);
				});
			}
		}
		window.ppSay('¡Mira bien y toca el que sea más grande o más pequeño!');
		next();
	}
</script>

<GameShell gameNum={15} title="Grande o Pequeño" icon="📏" initGame={initG15} />
