<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	const G22_DATA=[
		{w:'Grande',o:'Pequeño',e:'🐘↔🐭'},{w:'Caliente',o:'Frío',e:'🔥↔❄️'},
		{w:'Rápido',o:'Lento',e:'🐇↔🐢'},{w:'Alto',o:'Bajo',e:'🦒↔🐁'},
		{w:'Día',o:'Noche',e:'☀️↔🌙'},{w:'Feliz',o:'Triste',e:'😊↔😢'},
		{w:'Lleno',o:'Vacío',e:'🥛↔🫙'},{w:'Abierto',o:'Cerrado',e:'📖↔📕'},
		{w:'Nuevo',o:'Viejo',e:'✨↔🏚️'},{w:'Blando',o:'Duro',e:'☁️↔🪨'},
		{w:'Arriba',o:'Abajo',e:'⬆️↔⬇️'},{w:'Claro',o:'Oscuro',e:'💡↔🌑'},
		{w:'Largo',o:'Corto',e:'🐍↔🐛'},{w:'Gordo',o:'Flaco',e:'🐷↔🦩'},
		{w:'Limpio',o:'Sucio',e:'🧼↔🗑️'},{w:'Fuerte',o:'Débil',e:'💪↔🪶'},
	];

	function initG22(cont, lv) {
		let round = 0;
		const data = shuf(G22_DATA).slice(0, lerpParam(lv, 5, 8));

		cont.innerHTML = `<div class="ins">¡Encuentra el contrario!</div>
			<div class="pbar"><div class="pfill" id="g22pb" style="width:0%;background:var(--c2)"></div></div>
			<div class="g22-prompt" id="g22prompt"></div>
			<div class="g8-opts" id="g22opts"></div>`;

		function next() {
			if (round >= data.length) { const _lv = window.ppWin(); window.ppCelebrate('¡Conoces todos los opuestos! ↔️', 3, () => initG22(cont, window.ppGetLevel()), _lv); return; }
			cont.querySelector('#g22pb').style.width = (round/data.length*100)+'%';
			const d = data[round];
			const promptEl = cont.querySelector('#g22prompt');
			promptEl.innerHTML = '<div style="font-size:2.5rem;margin-bottom:8px">'+d.e.split('↔')[0]+'</div><div style="font-size:1.8rem;font-weight:900">'+d.w+'</div><div style="font-size:.8rem;color:var(--ink2);margin-top:4px">¿Cuál es su opuesto?</div>';
			const numOpts = lv<=3?2:lv<=7?3:4;
			const others = G22_DATA.filter(x => x.o !== d.o && x.w !== d.o).map(x => x.o);
			const wrongs = shuf(others).slice(0, numOpts-1);
			const optsEl = cont.querySelector('#g22opts'); optsEl.innerHTML = '';
			shuf([d.o, ...wrongs]).forEach(c => {
				const b = document.createElement('div'); b.className = 'g8-opt'; b.textContent = c;
				b.onclick = () => {
					if(c===d.o){b.style.background='#EFFFEF';b.style.borderColor='#6BCB77';window.ppBeep(880,.2);window.ppSay('¡Correcto! El opuesto de '+d.w+' es '+d.o);window.ppOnCorrect();round++;setTimeout(next,1100);}
					else{b.classList.add('err');setTimeout(()=>b.classList.remove('err'),400);window.ppOnWrong();window.ppBoo();window.ppSay('¡Inténtalo!');}
				};
				optsEl.appendChild(b);
			});
			window.ppSay('¿Cuál es el opuesto de '+d.w+'?');
		}
		next();
	}
</script>

<GameShell gameNum={22} title="Opuestos" icon="↔️" initGame={initG22} />
