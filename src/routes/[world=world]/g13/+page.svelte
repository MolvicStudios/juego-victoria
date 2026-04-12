<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	const G13_DATA=[
		{e:'🐶',w:'Perro'},{e:'🐱',w:'Gato'},{e:'🦁',w:'León'},{e:'🐘',w:'Elefante'},
		{e:'🐬',w:'Delfín'},{e:'🦋',w:'Mariposa'},{e:'🍕',w:'Pizza'},{e:'🍎',w:'Manzana'},
		{e:'🚀',w:'Cohete'},{e:'🏠',w:'Casa'},{e:'🌸',w:'Flor'},{e:'🚂',w:'Tren'},
		{e:'🍦',w:'Helado'},{e:'🌈',w:'Arco iris'},{e:'⭐',w:'Estrella'},{e:'🐸',w:'Rana'},
		{e:'🐷',w:'Cerdo'},{e:'🐻',w:'Oso'},{e:'🐢',w:'Tortuga'},{e:'🎸',w:'Guitarra'},
		{e:'🚗',w:'Coche'},{e:'✈️',w:'Avión'},{e:'🎈',w:'Globo'},{e:'🍌',w:'Plátano'},
	];

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG13(cont, lv) {
		let round=0;
		/** @type {{e:string,w:string}|null} */
		let current=null;
		const data=shuf(G13_DATA).slice(0,lerpParam(lv,5,8));

		cont.innerHTML = `<div class="ins">¡Escucha y toca la imagen correcta!</div>
			<div class="pbar" id="g13pb"><div class="pfill" style="background:var(--c5)"></div></div>
			<button class="g13-play" id="g13play">🔊 Repetir</button>
			<div class="g13-opts" id="g13opts"></div>`;

		/** @type {HTMLElement} */ (cont.querySelector('#g13play')).onclick = () => { if(current) window.ppSay(current.w); };

		/** @param {number} r @param {number} t */
		function setPbar(r,t){const f=/** @type {HTMLElement} */ (cont.querySelector('#g13pb .pfill'));f.style.width=(r/t*100)+'%';}

		function next(){
			if(round>=data.length){const _lv=window.ppWin();window.ppCelebrate('¡Tienes un oído genial! 🗣️',3,()=>initG13(cont,window.ppGetLevel()),_lv);return;}
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
				d.innerHTML='<span class="ico">'+o.e+'</span><p>'+o.w+'</p>';
				d.onclick=()=>{
					if(o.w===cur.w){d.style.background='#EFFFEF';d.style.borderColor='#6BCB77';
						window.ppBeep(880,.2);window.ppSay('¡Correcto! ¡'+o.w+'!');window.ppOnCorrect();round++;setTimeout(next,1000);
					}else{d.classList.add('err');setTimeout(()=>d.classList.remove('err'),400);window.ppOnWrong();window.ppBoo();window.ppSay('¡Inténtalo!');}
				};
				optsEl.appendChild(d);
			});
			const playBtn=/** @type {HTMLElement} */ (cont.querySelector('#g13play'));
			if(noRepeat){playBtn.style.display='none';}else{playBtn.style.display='';}
			setTimeout(()=>window.ppSay(cur.w),400);
		}
		window.ppSay('¡Escucha bien la palabra y toca la imagen correcta!');
		next();
	}
</script>

<GameShell gameNum={13} title="¿Qué Oyes?" icon="🗣️" initGame={initG13} />
