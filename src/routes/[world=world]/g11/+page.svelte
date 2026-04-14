<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	/** @type {(key: string, vars?: Record<string, string|number>) => string} */ const T = (key, vars) => window.ppT?.(key, vars) ?? key;

	const G11_FRUITS=['🍎','🍊','🍋','🍇','🍓','🍑','🍒','🫐'];

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG11(cont, lv) {
		let round=0;
		const total=lerpParam(lv,5,7);

		cont.innerHTML = `<div class="ins" id="g11ins"></div>
			<div class="pbar" id="g11pb"><div class="pfill" style="background:var(--c3)"></div></div>
			<div class="g11-visual" id="g11vis"></div><div class="g11-nums" id="g11nums"></div>`;

		/** @param {number} r @param {number} t */
		function setPbar(r,t){const f=/** @type {HTMLElement} */ (cont.querySelector('#g11pb .pfill'));f.style.width=(r/t*100)+'%';}

		function next(){
			if(round>=total){const _lv=window.ppWin();window.ppCelebrate(T('games.g11.win'),3,()=>initG11(cont,window.ppGetLevel()),_lv);return;}
			setPbar(round,total);
			const isResta=lv>=13;
			const maxSum=lv<=3?3:lv<=6?5:lv<=9?8:12;
			const numOpts=lv<=9?3:4;
			const fr=G11_FRUITS[Math.floor(Math.random()*G11_FRUITS.length)];
			const vis=/** @type {HTMLElement} */ (cont.querySelector('#g11vis')), numsEl=/** @type {HTMLElement} */ (cont.querySelector('#g11nums')), insEl=/** @type {HTMLElement} */ (cont.querySelector('#g11ins'));

			if(isResta){
				const a=Math.floor(Math.random()*7)+3;
				const b=Math.floor(Math.random()*Math.min(a-1,4))+1;
				const ans=a-b;
				insEl.textContent=T('games.g11.instruction_sub');
				vis.innerHTML='';
				for(let i=0;i<a;i++){const s=document.createElement('span');s.className='g11-fruit';s.textContent=fr;s.style.animationDelay=(i*.04)+'s';if(i>=a-b)s.style.cssText+='opacity:.3;text-decoration:line-through;';vis.appendChild(s);}
				const minus=document.createElement('span');minus.className='g11-op';minus.textContent='− '+b+' = ?';vis.appendChild(minus);
				numsEl.innerHTML='';
				const cols=['#FF6B6B','#4D9FEC','#6BCB77','#FF9F43'];
				const vals=[ans];while(vals.length<numOpts){const r2=Math.max(0,ans+Math.floor(Math.random()*5)-2);if(!vals.includes(r2))vals.push(r2);}
				shuf(vals).forEach((v,i)=>{
					const b2=document.createElement('button');b2.className='g11-num';b2.style.background=cols[i%4];b2.textContent=String(v);
					b2.onclick=()=>{
						if(v===ans){b2.style.background='#6BCB77';window.ppBeep(880,.2);window.ppSay(T('games.g11.correct_sub',{a,b,ans}));
							window.ppOnCorrect();round++;setTimeout(next,1000);
						}else{b2.classList.add('err');setTimeout(()=>b2.classList.remove('err'),400);window.ppOnWrong();window.ppBoo();window.ppSay(T('games.common.try_again'));}
					};
					numsEl.appendChild(b2);
				});
				window.ppSay(T('games.g11.prompt_sub',{a,b}));
			}else{
				const a=Math.floor(Math.random()*(maxSum-1))+1;
				const b=Math.floor(Math.random()*Math.min(maxSum-a,a+2))+1;
				const ans=a+b;
				insEl.textContent=T('games.g11.instruction_sum');
				vis.innerHTML='';
				for(let i=0;i<a;i++){const s=document.createElement('span');s.className='g11-fruit';s.textContent=fr;s.style.animationDelay=(i*.04)+'s';vis.appendChild(s);}
				const plus=document.createElement('span');plus.className='g11-op';plus.textContent='+';vis.appendChild(plus);
				for(let i=0;i<b;i++){const s=document.createElement('span');s.className='g11-fruit';s.textContent=fr;s.style.animationDelay=((a+i)*.04)+'s';vis.appendChild(s);}
				const eq=document.createElement('span');eq.className='g11-op';eq.textContent='= ?';vis.appendChild(eq);
				numsEl.innerHTML='';
				const cols=['#FF6B6B','#4D9FEC','#6BCB77','#FF9F43'];
				const vals=[ans];while(vals.length<numOpts){const r2=Math.max(1,ans+Math.floor(Math.random()*5)-2);if(!vals.includes(r2))vals.push(r2);}
				shuf(vals).forEach((v,i)=>{
					const b2=document.createElement('button');b2.className='g11-num';b2.style.background=cols[i%4];b2.textContent=String(v);
					b2.onclick=()=>{
						if(v===ans){b2.style.background='#6BCB77';window.ppBeep(880,.2);window.ppSay(T('games.g11.correct_sum',{a,b,ans}));
							window.ppOnCorrect();round++;setTimeout(next,1000);
						}else{b2.classList.add('err');setTimeout(()=>b2.classList.remove('err'),400);window.ppOnWrong();window.ppBoo();window.ppSay(T('games.common.try_again'));}
					};
					numsEl.appendChild(b2);
				});
				window.ppSay(T('games.g11.prompt_sum',{a,b}));
			}
		}
		window.ppSay(T('games.g11.hello'));
		next();
	}
</script>

<GameShell gameNum={11} title="Sumas Fáciles" icon="🧮" initGame={initG11} />
