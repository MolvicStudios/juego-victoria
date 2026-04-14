<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	const T = (key, vars) => window.ppT?.(key, vars) ?? key;

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG31(cont, lv) {
		let round = 0;
		const total = lerpParam(lv, 5, 8);

		cont.innerHTML = `<div class="ins">${T('games.g31.instruction')}</div>
			<div class="pbar"><div class="pfill" id="g31pb" style="width:0%;background:var(--c3)"></div></div>
			<div class="g31-seq" id="g31seq"></div>
			<div class="g8-opts" id="g31opts"></div>`;

		function genSeq() {
			const type = Math.floor(Math.random() * (lv<=3?1:lv<=7?2:4));
			let seq;
			const start = Math.floor(Math.random()*10)+1;
			const len = lerpParam(lv,4,6);
			if (type===0) { // +1
				seq = Array.from({length:len},(_,i)=>start+i);
			} else if (type===1) { // +2
				seq = Array.from({length:len},(_,i)=>start+i*2);
			} else if (type===2) { // +3 or +5
				const step = Math.random()<0.5?3:5;
				seq = Array.from({length:len},(_,i)=>start+i*step);
			} else { // *2
				const s = Math.floor(Math.random()*3)+1;
				seq = Array.from({length:len},(_,i)=>s*Math.pow(2,i));
			}
			const hideIdx = 1 + Math.floor(Math.random()*(seq.length-2)); // never hide first or last
			return {seq, hideIdx, ans: seq[hideIdx]};
		}

		function next() {
			if (round >= total) { const _lv = window.ppWin(); window.ppCelebrate(T('games.g31.win') + ' 🔢', 3, () => initG31(cont, window.ppGetLevel()), _lv); return; }
			/** @type {HTMLElement} */ (cont.querySelector('#g31pb')).style.width = (round/total*100)+'%';

			const {seq, hideIdx, ans} = genSeq();

			const seqEl = /** @type {HTMLElement} */ (cont.querySelector('#g31seq')); seqEl.innerHTML='';
			seq.forEach((n,i)=>{
				const s = document.createElement('span');
				s.className = 'g31-n' + (i===hideIdx?' g31-blank':'');
				s.textContent = i===hideIdx?'?':String(n);
				seqEl.appendChild(s);
			});

			const numOpts = lv<=3?2:lv<=7?3:4;
			const wrongs = new Set();
			while (wrongs.size < numOpts-1) {
				let w = ans + (Math.random()<0.5?1:-1)*(Math.floor(Math.random()*5)+1);
				if (w>0 && w!==ans) wrongs.add(w);
			}

			const optsEl = /** @type {HTMLElement} */ (cont.querySelector('#g31opts')); optsEl.innerHTML='';
			const cols = ['#FF6B6B','#4D9FEC','#6BCB77','#FF9F43'];
			shuf([ans,...wrongs]).forEach((v, i) => {
				const b = document.createElement('div');
				b.className = 'g2-num';
				b.style.background = cols[i % 4];
				b.textContent = String(v);
				b.onclick = () => {
					if (v===ans) {
						b.style.background='#EFFFEF'; b.style.borderColor='#6BCB77';
						seqEl.children[hideIdx].textContent = String(ans);
						seqEl.children[hideIdx].classList.remove('g31-blank');
						window.ppBeep(880,.2); window.ppSay(T('games.g31.correct', {n: ans})); window.ppOnCorrect(); round++; setTimeout(next,1200);
					} else { b.classList.add('err'); setTimeout(()=>b.classList.remove('err'),400); window.ppOnWrong(); window.ppBoo(); }
				};
				optsEl.appendChild(b);
			});
			window.ppSay(T('games.g31.hello'));
		}
		next();
	}
</script>

<GameShell gameNum={31} title="Secuencias" icon="🔢" initGame={initG31} />
