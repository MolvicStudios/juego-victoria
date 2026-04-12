<script>
	import GameShell from '$lib/components/GameShell.svelte';

	const G6_KEYS=[{n:'Do',f:261.63,c:'#FF6B6B'},{n:'Re',f:293.66,c:'#FF9F43'},{n:'Mi',f:329.63,c:'#FFD93D'},{n:'Fa',f:349.23,c:'#6BCB77'},{n:'Sol',f:392,c:'#4D9FEC'},{n:'La',f:440,c:'#A78BFA'},{n:'Si',f:493.88,c:'#F472B6'},{n:'Do²',f:523.25,c:'#2DD4BF'}];
	const G6_SONGS={1:{name:'Mini (5 notas)',notes:[0,0,4,4,0]},2:{name:'Campanitas',notes:[0,0,4,4,5,5,4,3,3,2,2,1,1,0]},3:{name:'Estrellita',notes:[0,0,4,4,5,5,4,3,3,2,2,1,1,0,4,4,3,3,2,2,1]},4:{name:'Cumpleaños',notes:[0,0,1,0,3,2,0,0,1,0,4,3,0,0,7,5,3,2,1]},5:{name:'La Vaca Lechera',notes:[0,0,4,4,5,5,4,3,3,2,2,1,1,0]},6:{name:'Desafío 1',notes:[0,2,4,5,4,2,0,1,3,5,6,5,3,1,0,4,7,4,0]},7:{name:'Al Corro',notes:[0,1,2,3,4,5,6,7,7,6,5,4,3,2,1,0,0,2,4,7]},8:{name:'Desafío 2',notes:[7,5,3,0,2,4,6,7,5,3,1,0,2,4,7,5,3,1,0,7]},9:{name:'Reto Final',notes:[0,0,4,4,5,5,4,3,3,2,2,1,1,0,7,7,5,5,3,3,1,0,2,4,7]}};
	let container, g6Mode='libre', g6SongNotes=[], g6NoteIdx=0, g6NumKeys=4;

	function initG6(cont, lv) {
		container = cont; g6Mode = 'libre'; g6NoteIdx = 0;
		const numKeys = lv<=3?4:lv<=6?6:8;
		g6NumKeys = numKeys;
		const W = Math.min(window.innerWidth-24, 440);
		const keyW = Math.floor((W-4*(numKeys-1))/numKeys);
		const keyH = Math.max(70, Math.floor(keyW*2.2));

		cont.innerHTML = `<div class="g6-modes"><button class="g6-mbtn on" id="g6mfree">🎹 Libre</button><button class="g6-mbtn" id="g6msong">🎼 Canción</button></div>
			<div class="ins" id="g6ins">¡Toca las teclas de colores!</div>
			<div class="g6-keys" id="g6keys"></div>
			<div class="g6-seq" id="g6seq" style="display:none"></div>
			<div class="g6-log" id="g6log">Toca una tecla...</div>`;

		cont.querySelector('#g6mfree').onclick = () => g6SetMode('libre');
		cont.querySelector('#g6msong').onclick = () => g6SetMode('cancion');

		const keysEl = cont.querySelector('#g6keys');
		for(let i=0;i<numKeys;i++){
			const k = G6_KEYS[i];
			const b = document.createElement('button'); b.className = 'g6-key'; b.id = 'g6k'+i;
			b.style.cssText = `background:${k.c};width:${keyW}px;height:${keyH}px;box-shadow:0 6px 0 ${k.c}88`;
			b.textContent = k.n;
			const play = () => {
				window.ppBeep(k.f,.5,'sine',.3); b.classList.add('press'); setTimeout(()=>b.classList.remove('press'),180);
				if(g6Mode==='libre'){window.ppSay(k.n);cont.querySelector('#g6log').textContent='🎵 '+k.n;}
				else g6CheckNote(i);
			};
			b.addEventListener('touchstart',e=>{e.preventDefault();play();},{passive:false});
			b.onmousedown = play;
			keysEl.appendChild(b);
		}
		window.ppSay('¡Toca las teclas de colores y haz música!');
	}

	function g6SetMode(mode) {
		g6Mode = mode;
		container.querySelector('#g6mfree').classList.toggle('on',mode==='libre');
		container.querySelector('#g6msong').classList.toggle('on',mode==='cancion');
		if(mode==='cancion'){
			const lv = window.ppGetLevel();
			const songIdx = Math.min(Math.ceil(lv/2), Object.keys(G6_SONGS).length);
			const song = G6_SONGS[songIdx]||G6_SONGS[1];
			g6SongNotes = song.notes.filter(n => n < g6NumKeys); g6NoteIdx = 0;
			container.querySelector('#g6ins').textContent = (lv<13?'¡Toca la tecla que brilla!':'¡Toca de memoria!')+' 🎼 '+song.name;
			const seqEl = container.querySelector('#g6seq'); seqEl.style.display = 'flex'; seqEl.innerHTML = '';
			song.notes.forEach((_,i) => { const d=document.createElement('div');d.className='g6-note';d.textContent=G6_KEYS[song.notes[i]]?.n||'?';d.id='g6seq'+i;seqEl.appendChild(d); });
			g6HighlightNext();
		} else {
			container.querySelector('#g6ins').textContent = '¡Toca las teclas!';
			container.querySelector('#g6seq').style.display = 'none';
			container.querySelectorAll('.g6-key').forEach(k=>k.classList.remove('glow'));
		}
	}

	function g6HighlightNext() {
		container.querySelectorAll('.g6-key').forEach(k=>k.classList.remove('glow'));
		container.querySelectorAll('.g6-note').forEach(n=>n.classList.remove('cur'));
		if(g6NoteIdx<g6SongNotes.length){
			const lv = window.ppGetLevel();
			if(lv<13){const keyEl=container.querySelector('#g6k'+g6SongNotes[g6NoteIdx]);if(keyEl)keyEl.classList.add('glow');}
			const seqEl=container.querySelector('#g6seq'+g6NoteIdx);if(seqEl)seqEl.classList.add('cur');
		}
	}

	function g6CheckNote(keyIdx) {
		if(keyIdx===g6SongNotes[g6NoteIdx]){
			const seqEl=container.querySelector('#g6seq'+g6NoteIdx);if(seqEl){seqEl.classList.add('done');seqEl.classList.remove('cur');}
			g6NoteIdx++;
			if(g6NoteIdx>=g6SongNotes.length){
				container.querySelectorAll('.g6-key').forEach(k=>k.classList.remove('glow'));
				window.ppOnCorrect();const _lv=window.ppWin();setTimeout(()=>window.ppCelebrate('¡Tocaste la canción! 🎵🎶',3,()=>initG6(container,window.ppGetLevel()),_lv),300);
			} else { setTimeout(g6HighlightNext, window.ppGetLevel()>=10?100:250); }
		} else { window.ppOnWrong(); window.ppBoo(); window.ppSay('¡Toca la tecla correcta!'); }
	}
</script>

<GameShell gameNum={6} title="Piano Mágico" icon="🎵" initGame={initG6} />
