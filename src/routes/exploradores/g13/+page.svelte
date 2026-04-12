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

	function initG13(cont, lv) {
		let round=0, current=null;
		const data=shuf(G13_DATA).slice(0,lerpParam(lv,5,8));

		cont.innerHTML = `<div class="ins">¡Escucha y toca la imagen correcta!</div>
			<div class="pbar" id="g13pb"><div class="pbar-f"></div></div>
			<button class="g13-play" id="g13play">🔊 Repetir</button>
			<div class="g13-opts" id="g13opts"></div>`;

		cont.querySelector('#g13play').onclick = () => { if(current) window.ppSay(current.w); };

		function setPbar(r,t){const f=cont.querySelector('#g13pb .pbar-f');if(f)f.style.width=(r/t*100)+'%';}

		function next(){
			if(round>=data.length){const _lv=window.ppWin();window.ppCelebrate('¡Tienes un oído genial! 🗣️',3,()=>initG13(cont,window.ppGetLevel()),_lv);return;}
			setPbar(round,data.length);
			current=data[round];
			const numOpts=lv<=3?2:lv<=7?3:4;
			const noRepeat=lv>=12;
			const others=G13_DATA.filter(d=>d.w!==current.w);
			const opts=shuf([current,...shuf(others).slice(0,numOpts-1)]);
			const optsEl=cont.querySelector('#g13opts');optsEl.innerHTML='';
			opts.forEach(o=>{
				const d=document.createElement('div');d.className='g13-opt';
				d.innerHTML='<span class="ico">'+o.e+'</span><p>'+o.w+'</p>';
				d.onclick=()=>{
					if(o.w===current.w){d.style.background='#EFFFEF';d.style.borderColor='#6BCB77';
						window.ppBeep(880,.2);window.ppSay('¡Correcto! ¡'+o.w+'!');window.ppOnCorrect();round++;setTimeout(next,1000);
					}else{d.classList.add('err');setTimeout(()=>d.classList.remove('err'),400);window.ppOnWrong();window.ppBoo();window.ppSay('¡Inténtalo!');}
				};
				optsEl.appendChild(d);
			});
			if(noRepeat){cont.querySelector('#g13play').style.display='none';}else{cont.querySelector('#g13play').style.display='';}
			setTimeout(()=>{
				if(window.speechSynthesis){
					speechSynthesis.cancel();
					const u=new SpeechSynthesisUtterance(current.w);
					u.lang='es-ES';u.rate=lv<=3?0.7:0.85;u.pitch=1.15;
					speechSynthesis.speak(u);
				}
			},400);
		}
		window.ppSay('¡Escucha bien la palabra y toca la imagen correcta!');
		next();
	}
</script>

<GameShell gameNum={13} title="¿Qué Oyes?" icon="🗣️" initGame={initG13} />
