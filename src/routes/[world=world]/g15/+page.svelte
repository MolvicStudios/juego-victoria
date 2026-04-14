<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	/** @type {(key: string, vars?: Record<string, string|number>) => string} */ const T = (key, vars) => window.ppT?.(key, vars) ?? key;

	const G15_SETS=[
		{items:[{e:'🐘',n:'elephant'},{e:'🐶',n:'dog'},{e:'🐭',n:'mouse'},{e:'🐜',n:'ant'}]},
		{items:[{e:'🌳',n:'tree'},{e:'🌻',n:'sunflower'},{e:'🌸',n:'flower'},{e:'🌱',n:'seed'}]},
		{items:[{e:'🚌',n:'bus'},{e:'🚗',n:'car'},{e:'🛵',n:'motorcycle'},{e:'🛴',n:'scooter'}]},
		{items:[{e:'🏔️',n:'mountain'},{e:'🏠',n:'house'},{e:'⛺',n:'tent'},{e:'📦',n:'box'}]},
		{items:[{e:'🐋',n:'whale'},{e:'🐬',n:'dolphin'},{e:'🐟',n:'fish'},{e:'🦐',n:'shrimp'}]},
		{items:[{e:'🚀',n:'rocket'},{e:'✈️',n:'plane'},{e:'🦋',n:'butterfly'},{e:'🐝',n:'bee'}]},
		{items:[{e:'🌞',n:'sun'},{e:'🌙',n:'moon'},{e:'⭐',n:'little_star'},{e:'✨',n:'spark'}]},
		{items:[{e:'🏰',n:'castle'},{e:'🏠',n:'little_house'},{e:'🎩',n:'hat'},{e:'🧢',n:'cap'}]},
		{items:[{e:'🦕',n:'dinosaur'},{e:'🐊',n:'crocodile'},{e:'🦎',n:'lizard'},{e:'🐛',n:'worm'}]},
		{items:[{e:'🎪',n:'circus'},{e:'🎡',n:'ferris_wheel'},{e:'🎠',n:'carousel'},{e:'🪁',n:'kite'}]},
	];
	const G15_SIZES=['5.4rem','3rem','1.7rem','1rem'];

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG15(cont, lv) {
		let round=0;
		const total=lerpParam(lv,5,7);

		cont.innerHTML = `<div class="ins" id="g15ins"></div>
			<div class="pbar" id="g15pb"><div class="pfill" style="background:var(--c6)"></div></div>
			<div class="g15-objects" id="g15objects"></div>`;

		/** @param {number} r @param {number} t */
		function setPbar(r,t){const f=/** @type {HTMLElement} */ (cont.querySelector('#g15pb .pfill'));f.style.width=(r/t*100)+'%';}

		function next(){
			if(round>=total){const _lv=window.ppWin();window.ppCelebrate(T('games.g15.win'),3,()=>initG15(cont,window.ppGetLevel()),_lv);return;}
			setPbar(round,total);
			const numItems=lv<=6?2:lv<=12?3:4;
			const set=G15_SETS[Math.floor(Math.random()*G15_SETS.length)];
			const items=set.items.slice(0,Math.min(numItems,set.items.length));
			/** @type {string} */
			let askType;
			/** @type {string} */
			let correctName;
			/** @type {string} */
			let qTxt;

			if(lv<=3){askType='big';correctName=items[0].n;qTxt=T('games.g15.q_biggest');}
			else if(lv<=6){askType=Math.random()>.5?'big':'small';correctName=askType==='big'?items[0].n:items[items.length-1].n;qTxt=askType==='big'?T('games.g15.q_biggest'):T('games.g15.q_smallest');}
			else if(lv<=9){askType=Math.random()>.5?'big':'small';correctName=askType==='big'?items[0].n:items[items.length-1].n;qTxt=askType==='big'?T('games.g15.q_biggest'):T('games.g15.q_smallest');}
			else if(lv<=12){askType='medium';correctName=items[1].n;qTxt=T('games.g15.q_medium');}
			else{askType='order';qTxt=T('games.g15.q_order');}

			const qEl=/** @type {HTMLElement} */ (cont.querySelector('#g15ins'));qEl.textContent=qTxt;
			qEl.style.color=askType==='big'?'var(--c1)':askType==='small'?'var(--c5)':'var(--c6)';
			window.ppSay(qTxt.replace(/[👆👇🤔]/g,''));

			const vEl=/** @type {HTMLElement} */ (cont.querySelector('#g15objects'));vEl.innerHTML='';

			if(askType==='order'){
				let orderIdx=0;
				const displayed=shuf(items.map((it,i)=>({...it,sizeIdx:i})));
				displayed.forEach(it=>{
					const d=document.createElement('div');d.className='g15-obj';
					const emo=document.createElement('span');emo.className='g15-emo';emo.style.fontSize=G15_SIZES[it.sizeIdx];emo.textContent=it.e;
					const lbl=document.createElement('span');lbl.className='g15-lbl';lbl.textContent=T('games.g15.items.'+it.n);
					d.appendChild(emo);d.appendChild(lbl);
					d.onclick=()=>{
						if(it.sizeIdx===orderIdx){d.classList.add('hit-ok');d.style.pointerEvents='none';window.ppBeep(880,.15);orderIdx++;
							if(orderIdx>=items.length){window.ppOnCorrect();round++;setTimeout(next,700);}
						}else{d.classList.add('hit-err');setTimeout(()=>d.classList.remove('hit-err'),400);window.ppOnWrong();window.ppBoo();window.ppSay(T('games.g15.find_biggest'));}
					};
					vEl.appendChild(d);
				});
			}else{
				const displayed=shuf(items.map((it,i)=>({...it,sizeIdx:i})));
				displayed.forEach(it=>{
					const d=document.createElement('div');d.className='g15-obj';
					const emo=document.createElement('span');emo.className='g15-emo';emo.style.fontSize=G15_SIZES[it.sizeIdx];emo.textContent=it.e;
					const lbl=document.createElement('span');lbl.className='g15-lbl';if(lv>=3)lbl.textContent=T('games.g15.items.'+it.n);
					d.appendChild(emo);d.appendChild(lbl);
					d.onclick=()=>{
						if(it.n===correctName){d.classList.add('hit-ok');window.ppBeep(880,.22);window.ppSay(T('games.g15.correct',{name:T('games.g15.items.'+it.n)}));window.ppOnCorrect();round++;setTimeout(next,950);}
						else{d.classList.add('hit-err');setTimeout(()=>d.classList.remove('hit-err'),400);window.ppOnWrong();window.ppBoo();window.ppSay(T('games.g15.look_size'));}
					};
					vEl.appendChild(d);
				});
			}
		}
		window.ppSay(T('games.g15.hello'));
		next();
	}
</script>

<GameShell gameNum={15} title="Grande o Pequeño" icon="📏" initGame={initG15} />
