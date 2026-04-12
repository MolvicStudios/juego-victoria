<script>
	import { onDestroy } from 'svelte';
	import GameShell from '$lib/components/GameShell.svelte';
	import { shuf, lerpParam } from '$lib/data.js';

	const G5_ANIM=['🐶','🐱','🐻','🐼','🦊','🐸','🦁','🐨','🐯','🐰','🐮','🐷'];
	let container, g5Flipped=[], g5Matched=0, g5CanFlip=true, g5Timer=null, g5Sec=0;

	function initG5(cont, lv) {
		container = cont; g5Flipped=[]; g5Matched=0; g5CanFlip=true; g5Sec=0;
		if(g5Timer) clearInterval(g5Timer);
		const pairCount = lv<=3?lerpParam(lv,2,2):lv<=6?3:lv<=9?4:lv<=12?6:8;
		const animals = shuf(G5_ANIM).slice(0, pairCount);
		const cards = shuf([...animals,...animals]);
		const cols = lv<=3?2:lv<=6?3:lv<=9?(pairCount<=4?2:4):4;

		cont.innerHTML = `<div class="ins">¡Encuentra las parejas!</div>
			<div style="display:flex;gap:12px;align-items:center"><div style="--color:var(--c5)" class="badge">⭐ <span id="g5sc">0</span></div><div class="g5-timer" id="g5timer"></div></div>
			<div class="g5-grid" id="g5grid"></div>`;

		const gr = cont.querySelector('#g5grid');
		const cardW = Math.min(Math.floor((Math.min(window.innerWidth,440)-20-7*(cols-1))/cols),85);
		gr.style.gridTemplateColumns = `repeat(${cols},1fr)`;
		gr.style.maxWidth = (cardW*cols+7*(cols-1))+'px';

		cards.forEach(em => {
			const c = document.createElement('div'); c.className = 'g5-card'; c.dataset.v = em;
			c.innerHTML = '<div class="g5-front">?</div><div class="g5-back">'+em+'</div>';
			c.onclick = () => g5Flip(c);
			gr.appendChild(c);
		});

		if(lv>=10) g5Timer = setInterval(() => { g5Sec++; cont.querySelector('#g5timer').textContent = '⏱️ '+g5Sec+'s'; }, 1000);
		window.ppSay('¡Toca las cartas y encuentra las parejas iguales!');
	}

	function g5Flip(card) {
		if(!g5CanFlip||card.classList.contains('flip')||card.classList.contains('mat')) return;
		if(g5Flipped.length===1&&card===g5Flipped[0]) return;
		card.classList.add('flip'); window.ppBeep(500+g5Flipped.length*100,.1); g5Flipped.push(card);
		if(g5Flipped.length===2){
			g5CanFlip=false; const[a,b]=g5Flipped;
			if(a.dataset.v===b.dataset.v){
				a.classList.add('mat');b.classList.add('mat');
				g5Matched++; container.querySelector('#g5sc').textContent=g5Matched;
				window.ppBeep(880,.2); window.ppSay('¡Pareja!'); g5Flipped=[]; g5CanFlip=true;
				window.ppOnCorrect();
				if(g5Matched===container.querySelectorAll('.g5-card').length/2){
					if(g5Timer) clearInterval(g5Timer);
					const _lv=window.ppWin();
					setTimeout(()=>window.ppCelebrate('¡Todas las parejas! 🃏',3,()=>initG5(container,window.ppGetLevel()),_lv),400);
				}
			} else {
				setTimeout(()=>{a.classList.remove('flip');b.classList.remove('flip');g5Flipped=[];g5CanFlip=true;window.ppOnWrong();window.ppBoo();},900);
			}
		}
	}

	onDestroy(() => { if(g5Timer) clearInterval(g5Timer); });
</script>

<GameShell gameNum={5} title="Memoria" icon="🃏" initGame={initG5} />
