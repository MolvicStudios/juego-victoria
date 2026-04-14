<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	const T = (key, vars) => window.ppT?.(key, vars) ?? key;

	const G8_DATA=[
		{e:'🦁',key:'lion',x:['tiger','bear','wolf']},{e:'🐘',key:'elephant',x:['giraffe','hippo','rhino']},
		{e:'🍎',key:'apple',x:['pear','orange','cherry']},{e:'🚀',key:'rocket',x:['plane','balloon','helicopter']},
		{e:'🌈',key:'rainbow',x:['cloud','storm','rain']},{e:'🐬',key:'dolphin',x:['whale','shark','fish']},
		{e:'🍕',key:'pizza',x:['burger','pasta','sandwich']},{e:'🦋',key:'butterfly',x:['bee','dragonfly','fly']},
		{e:'🏠',key:'house',x:['castle','building','cabin']},{e:'🌸',key:'flower',x:['tree','grass','cactus']},
		{e:'🚂',key:'train',x:['car','ship','bicycle']},{e:'🍦',key:'icecream',x:['cake','cookie','chocolate']},
		{e:'🐢',key:'turtle',x:['snail','frog','lizard']},{e:'⭐',key:'star',x:['moon','sun','planet']},
		{e:'🎸',key:'guitar',x:['piano','drum','flute']},
	];

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG8(cont, lv) {
		let round = 0;
		const data = shuf(G8_DATA).slice(0, lerpParam(lv,5,8));

		cont.innerHTML = `<div class="ins">${T('games.g8.instruction')}</div>
			<div class="pbar" id="g8pb"><div class="pfill" style="background:var(--c1)"></div></div>
			<div class="g8-emo" id="g8emo"></div><div class="g8-opts" id="g8opts"></div>`;

		/** @param {number} r @param {number} t */
		function setPbar(r,t){const f=/** @type {HTMLElement} */ (cont.querySelector('#g8pb .pfill'));f.style.width=(r/t*100)+'%';}

		function next() {
			if(round>=data.length){const _lv=window.ppWin();window.ppCelebrate(T('games.g8.win')+' 📚',3,()=>initG8(cont,window.ppGetLevel()),_lv);return;}
			setPbar(round,data.length);
			const d=data[round];
			const audioOnly=lv>=12;
			const ee=/** @type {HTMLElement} */ (cont.querySelector('#g8emo'));ee.textContent=d.e;ee.style.animation='none';void ee.offsetWidth;ee.style.animation='popIn .35s';
			ee.style.visibility=audioOnly?'hidden':'';

			const numWrong=lv<=3?1:lv<=7?2:3;
			const wrongs=d.x.slice(0,numWrong);
			const optsEl=/** @type {HTMLElement} */ (cont.querySelector('#g8opts'));optsEl.innerHTML='';
			shuf([d.key,...wrongs]).forEach(c=>{
				const label=c===d.key?T('games.g8.words.'+c):T('games.g8.wrong.'+c);
				const b=document.createElement('div');b.className='g8-opt';b.textContent=label;
				b.onclick=()=>{
					if(c===d.key){b.style.background='#EFFFEF';b.style.borderColor='#6BCB77';
						window.ppBeep(880,.2);window.ppSay(T('games.g8.correct',{word:T('games.g8.words.'+d.key)}));window.ppOnCorrect();round++;setTimeout(next,900);
					}else{b.classList.add('err');setTimeout(()=>b.classList.remove('err'),400);window.ppOnWrong();window.ppBoo();window.ppSay(T('games.common.try_again'));}
				};
				optsEl.appendChild(b);
			});
			if(audioOnly){window.ppSay(T('games.g8.listen'));setTimeout(()=>window.ppSay(T('games.g8.words.'+d.key)),600);}else{window.ppSay(T('games.g8.what_is'));}
		}
		window.ppSay(T('games.g8.hello'));
		next();
	}
</script>

<GameShell gameNum={8} title="¿Qué Ves?" icon="👀" initGame={initG8} />
