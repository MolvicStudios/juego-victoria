<script>
	import { onDestroy } from 'svelte';
	import GameShell from '$lib/components/GameShell.svelte';
	import { shuf, lerpParam } from '$lib/data.js';

	const G2_FRUITS = ['🍎','🍊','🍋','🍇','🍓','🍑','🍒','🫐','🍌','🥝'];
	let container, g2Round = 0, g2Total = 5;

	function initG2(cont, lv) {
		container = cont; g2Round = 0; g2Total = lerpParam(lv, 5, 8);
		window.ppSay('¡Hola! ¡Toca cada fruta para contarla y elige el número correcto!');
		g2Next(lv);
	}

	function setPbar(id, val, max) { const el = container?.querySelector('#'+id); if(el) el.style.width = (val/max*100)+'%'; }

	function g2Next(lv) {
		if (!lv) lv = window.ppGetLevel();
		if (g2Round >= g2Total) { const _lv = window.ppWin(); window.ppCelebrate('¡Eres un genio contando! 🍎', 3, () => initG2(container, window.ppGetLevel()), _lv); return; }
		setPbar('g2pb', g2Round, g2Total);
		const maxCount = lv<=3?3:lv<=6?5:lv<=9?7:lv<=12?9:12;
		const numOpts = lv<=3?2:lv<=9?3:4;
		const n = Math.floor(Math.random()*maxCount)+1;
		const fr = G2_FRUITS[Math.floor(Math.random()*G2_FRUITS.length)];
		let tapped = 0;

		container.innerHTML = `
			<div class="pbar"><div class="pfill" id="g2pb" style="width:0%;background:var(--c2)"></div></div>
			<div class="ins" id="g2ins">¡Toca cada fruta para contarla!</div>
			<div class="g2-fruits" id="g2fruits"></div>
			<div class="g2-nums" id="g2nums" style="display:none"></div>`;
		setPbar('g2pb', g2Round, g2Total);

		const fruitsEl = container.querySelector('#g2fruits');
		const numsEl = container.querySelector('#g2nums');
		const insEl = container.querySelector('#g2ins');

		let isSum = lv>=10&&n>=2&&Math.random()>.3;
		let isResta = lv>=13&&n>=3&&Math.random()>.4;
		if (isResta) isSum = false;

		if (isResta) {
			const sumA = n+Math.floor(Math.random()*3)+1, sumB = sumA-n;
			insEl.textContent = sumA+' '+fr+' menos '+sumB+'. ¿Cuántas quedan?';
			const gd = document.createElement('div'); gd.style.cssText = 'display:flex;align-items:center;gap:8px;flex-wrap:wrap;justify-content:center';
			for(let i=0;i<sumA;i++){const d=document.createElement('div');d.className='g2-fr';d.textContent=fr;gd.appendChild(d);}
			const m = document.createElement('span'); m.style.cssText = 'font-size:2rem;font-weight:900;color:var(--ink)'; m.textContent = '−'; gd.appendChild(m);
			for(let i=0;i<sumB;i++){const d=document.createElement('div');d.className='g2-fr';d.textContent=fr;d.style.cssText='opacity:.4;text-decoration:line-through';gd.appendChild(d);}
			fruitsEl.appendChild(gd);
			numsEl.style.display = 'flex'; g2ShowNums(n, numOpts, numsEl);
		} else if (isSum) {
			const sumA = Math.floor(Math.random()*(n-1))+1, sumB = n-sumA;
			insEl.textContent = sumA+' '+fr+' y '+sumB+' más. ¿Cuántas hay?';
			const gd = document.createElement('div'); gd.style.cssText = 'display:flex;align-items:center;gap:8px;flex-wrap:wrap;justify-content:center';
			const gA = document.createElement('div'); gA.style.cssText = 'display:flex;gap:4px;flex-wrap:wrap;padding:8px;background:rgba(0,0,0,.03);border-radius:12px';
			for(let i=0;i<sumA;i++){const d=document.createElement('div');d.className='g2-fr';d.textContent=fr;gA.appendChild(d);}
			gd.appendChild(gA);
			const plus = document.createElement('span'); plus.style.cssText = 'font-size:2rem;font-weight:900;color:var(--ink)'; plus.textContent = '+'; gd.appendChild(plus);
			const gB = document.createElement('div'); gB.style.cssText = 'display:flex;gap:4px;flex-wrap:wrap;padding:8px;background:rgba(0,0,0,.03);border-radius:12px';
			for(let i=0;i<sumB;i++){const d=document.createElement('div');d.className='g2-fr';d.textContent=fr;gB.appendChild(d);}
			gd.appendChild(gB);
			fruitsEl.appendChild(gd);
			numsEl.style.display = 'flex'; g2ShowNums(n, numOpts, numsEl);
		} else {
			for(let i=0;i<n;i++){
				const d = document.createElement('div'); d.className = 'g2-fr'; d.textContent = fr;
				d.onclick = function() {
					if(this.classList.contains('tap')) return;
					this.classList.add('tap'); tapped++; window.ppBeep(300+tapped*60,.1); window.ppSay(tapped+'');
					if(tapped===n){ insEl.textContent = '¿Cuántas eran? ¡Elige!'; setTimeout(() => { numsEl.style.display = 'flex'; g2ShowNums(n, numOpts, numsEl); }, 400); }
				};
				fruitsEl.appendChild(d);
			}
			window.ppSay('¡Toca cada fruta!');
		}
	}

	function g2ShowNums(n, numOpts, numsEl) {
		const cols = ['#FF6B6B','#4D9FEC','#6BCB77','#FF9F43'];
		const vals = [n]; let tries=0; while(vals.length<numOpts&&tries<50){tries++;const r=Math.max(1,n+Math.floor(Math.random()*7)-3);if(!vals.includes(r)&&r!==n)vals.push(r);} while(vals.length<numOpts){vals.push(vals[vals.length-1]+1);}
		numsEl.innerHTML = '';
		shuf(vals).forEach((v,i) => {
			const b = document.createElement('button'); b.className = 'g2-num'; b.style.background = cols[i%4]; b.textContent = v;
			b.onclick = () => {
				if(v===n){b.style.background='#6BCB77';window.ppBeep(880,.2);window.ppSay('¡Correcto! ¡'+n+'!');window.ppOnCorrect();g2Round++;setTimeout(()=>g2Next(),900);}
				else{b.classList.add('err');setTimeout(()=>b.classList.remove('err'),400);window.ppOnWrong();window.ppBoo();window.ppSay('¡Inténtalo!');}
			};
			numsEl.appendChild(b);
		});
	}
</script>

<GameShell gameNum={2} title="Contar y Tocar" icon="🍎" initGame={initG2} />
