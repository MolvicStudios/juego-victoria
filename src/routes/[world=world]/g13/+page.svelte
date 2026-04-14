<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	const T = (key, vars) => window.ppT?.(key, vars) ?? key;

	const G13_DATA=[
		{e:'🐶',w:'dog'},{e:'🐱',w:'cat'},{e:'🦁',w:'lion'},{e:'🐘',w:'elephant'},
		{e:'🐬',w:'dolphin'},{e:'🦋',w:'butterfly'},{e:'🍕',w:'pizza'},{e:'🍎',w:'apple'},
		{e:'🚀',w:'rocket'},{e:'🏠',w:'house'},{e:'🌸',w:'flower'},{e:'🚂',w:'train'},
		{e:'🍦',w:'icecream'},{e:'🌈',w:'rainbow'},{e:'⭐',w:'star'},{e:'🐸',w:'frog'},
		{e:'🐷',w:'pig'},{e:'🐻',w:'bear'},{e:'🐢',w:'turtle'},{e:'🎸',w:'guitar'},
		{e:'🚗',w:'car'},{e:'✈️',w:'plane'},{e:'🎈',w:'balloon'},{e:'🍌',w:'banana'},
	];

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG13(cont, lv) {
		let round=0;
		/** @type {{e:string,w:string}|null} */
		let current=null;
		const data=shuf(G13_DATA).slice(0,lerpParam(lv,5,8));

		cont.innerHTML = `<div class="ins">${T('games.g13.instruction')}</div>
			<div class="pbar" id="g13pb"><div class="pfill" style="background:var(--c5)"></div></div>
			<button class="g13-play" id="g13play">${T('games.g13.repeat')}</button>
			<div class="g13-opts" id="g13opts"></div>`;

		/** @type {HTMLElement} */ (cont.querySelector('#g13play')).onclick = () => { if(current) window.ppSay(T('games.g13.words.'+current.w)); };

		/** @param {number} r @param {number} t */
		function setPbar(r,t){const f=/** @type {HTMLElement} */ (cont.querySelector('#g13pb .pfill'));f.style.width=(r/t*100)+'%';}

		function next(){
			if(round>=data.length){const _lv=window.ppWin();window.ppCelebrate(T('games.g13.win'),3,()=>initG13(cont,window.ppGetLevel()),_lv);return;}
			setPbar(round,data.length);
			current=data[round];
			const cur = /** @type {{e:string,w:string}} */ (current);
			const numOpts=lv<=3?2:lv<=7?3:4;
			const noRepeat=lv>=12;
			const others=G13_DATA.filter(d=>d.w!==cur.w);
			const opts=shuf([cur,...shuf(others).slice(0,numOpts-1)]);
			const optsEl=/** @type {HTMLElement} */ (cont.querySelector('#g13opts'));optsEl.innerHTML='';
			opts.forEach(o=>{
				const d=document.createElement('div');d.className='g13-opt';
				d.innerHTML='<span class="ico">'+o.e+'</span><p>'+T('games.g13.words.'+o.w)+'</p>';
				d.onclick=()=>{
					if(o.w===cur.w){d.style.background='#EFFFEF';d.style.borderColor='#6BCB77';
						window.ppBeep(880,.2);window.ppSay(T('games.g13.correct',{word:T('games.g13.words.'+o.w)}));window.ppOnCorrect();round++;setTimeout(next,1000);
					}else{d.classList.add('err');setTimeout(()=>d.classList.remove('err'),400);window.ppOnWrong();window.ppBoo();window.ppSay(T('games.common.try_again'));}
				};
				optsEl.appendChild(d);
			});
			const playBtn=/** @type {HTMLElement} */ (cont.querySelector('#g13play'));
			if(noRepeat){playBtn.style.display='none';}else{playBtn.style.display='';}
			setTimeout(()=>window.ppSay(T('games.g13.words.'+cur.w)),400);
		}
		window.ppSay(T('games.g13.hello'));
		next();
	}
</script>

<GameShell gameNum={13} title="¿Qué Oyes?" icon="🗣️" initGame={initG13} />
