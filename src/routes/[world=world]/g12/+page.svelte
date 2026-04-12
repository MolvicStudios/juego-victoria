<script>
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam, shuf } from '$lib/data.js';

	const G12_PATHS={
		'A':[[50,5],[15,95],[32,58],[68,58],[85,95]],
		'E':[[70,5],[15,5],[15,95],[70,95],[15,50],[62,50]],
		'I':[[25,5],[75,5],[50,5],[50,95],[25,95],[75,95]],
		'O':[[50,5],[82,22],[82,78],[50,95],[18,78],[18,22],[50,5]],
		'U':[[20,5],[20,78],[50,95],[80,78],[80,5]],
		'M':[[15,95],[15,5],[50,58],[85,5],[85,95]],
		'P':[[20,95],[20,5],[65,5],[80,30],[65,50],[20,50]],
		'S':[[75,18],[55,5],[25,18],[28,50],[72,62],[72,82],[50,95],[22,85]],
		'L':[[20,5],[20,95],[75,95]],
		'T':[[15,5],[85,5],[50,5],[50,95]],
		'C':[[80,18],[52,5],[20,28],[20,72],[52,95],[80,82]],
		'D':[[20,5],[65,5],[82,28],[82,72],[65,95],[20,95],[20,5]],
		'N':[[15,95],[15,5],[85,95],[85,5]],
		'V':[[15,5],[50,95],[85,5]],
		'B':[[20,95],[20,5],[60,5],[78,18],[60,50],[78,72],[60,95],[20,95]],
		'F':[[70,5],[20,5],[20,95],[20,50],[60,50]],
		'G':[[75,18],[50,5],[22,28],[22,72],[50,95],[78,72],[78,50],[50,50]],
		'H':[[20,5],[20,95],[20,50],[80,50],[80,5],[80,95]],
		'J':[[65,5],[65,78],[50,95],[30,88]],
		'K':[[20,5],[20,95],[20,52],[75,5],[20,52],[75,95]],
		'R':[[20,95],[20,5],[65,5],[80,25],[65,50],[20,50],[65,50],[80,95]],
		'1':[[35,18],[50,5],[50,95]],
		'2':[[18,28],[40,5],[70,5],[82,30],[50,55],[18,95],[82,95]],
		'3':[[18,15],[50,5],[82,22],[50,50],[82,78],[50,95],[18,85]],
		'4':[[15,62],[62,5],[62,95]],
		'5':[[72,5],[22,5],[18,48],[60,42],[78,58],[72,82],[50,95],[22,88]],
		'6':[[65,10],[40,5],[20,30],[20,70],[40,95],[65,85],[70,60],[40,50],[20,60]],
		'7':[[18,5],[82,5],[50,95]],
		'8':[[50,5],[75,18],[50,48],[25,18],[50,5],[25,75],[50,95],[75,75],[50,48]],
		'9':[[65,50],[45,40],[25,20],[45,5],[70,20],[70,50],[55,85],[35,95]],
	};

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG12(cont, lv) {
		let round=0;
		/** @type {number[][]} */
		let curPts=[];
		let ptIdx=0;
		/** @type {CanvasRenderingContext2D|null} */
		let ctx=null;
		let pool;
		if(lv<=3)pool=['A','E','I','O','U'];
		else if(lv<=6)pool=['M','P','S','L','T'];
		else if(lv<=9)pool=['B','C','D','F','G','N','R','H'];
		else if(lv<=12)pool=['1','2','3','4','5','6','7','8','9'];
		else pool=['O','S','M','I','L','A'];
		const data=shuf(pool).slice(0,lerpParam(lv,4,6));

		cont.innerHTML = `<div class="ins">¡Toca los puntos en orden!</div>
			<div class="pbar" id="g12pb"><div class="pfill" style="background:var(--c4)"></div></div>
			<div class="g12-letter-display" id="g12letter"></div>
			<div class="g12-wrap"><canvas id="g12cvs"></canvas></div>`;

		/** @param {number} r @param {number} t */
		function setPbar(r,t){const f=/** @type {HTMLElement} */ (cont.querySelector('#g12pb .pfill'));f.style.width=(r/t*100)+'%';}

		function drawDots(){
			const c = ctx;
			if(!c) return;
			curPts.forEach((p,i)=>{
				const done=i<ptIdx, current=i===ptIdx;
				if(done&&i>0){c.beginPath();c.moveTo(curPts[i-1][0],curPts[i-1][1]);c.lineTo(p[0],p[1]);c.strokeStyle='#6BCB77';c.lineWidth=6;c.lineCap='round';c.stroke();}
				c.beginPath();c.arc(p[0],p[1],current?16:12,0,Math.PI*2);
				c.fillStyle=done?'#6BCB77':current?'#FF6B6B':'#CCC';c.fill();
				if(lv<=6||done){c.fillStyle='#fff';c.font='bold 11px Nunito,sans-serif';c.textAlign='center';c.textBaseline='middle';c.fillText(String(i+1),p[0],p[1]);}
			});
		}

		/** @param {{clientX:number,clientY:number}} touch @param {HTMLCanvasElement} cvs */
		function handleTouch(touch,cvs){
			const c = ctx;
			if(!c) return;
			const r2=cvs.getBoundingClientRect();
			const x=touch.clientX-r2.left, y=touch.clientY-r2.top;
			if(ptIdx>=curPts.length)return;
			const tp=curPts[ptIdx];
			const dist=Math.sqrt((x-tp[0])**2+(y-tp[1])**2);
			if(dist<cvs.width*.07){
				ptIdx++;window.ppBeep(400+ptIdx*50,.1);
				const W=cvs.width,H=cvs.height;
				c.fillStyle='#F5F5F5';c.fillRect(0,0,W,H);
				const letter=data[round];
				c.font=`bold ${H*.75}px Nunito,sans-serif`;c.fillStyle='#DEDEDE';c.textAlign='center';c.textBaseline='middle';
				c.fillText(letter,W/2,H/2);
				drawDots();
				if(ptIdx>=curPts.length){
					window.ppOnCorrect();round++;
					setTimeout(()=>{
						if(round>=data.length){const _lv=window.ppWin();window.ppCelebrate('¡Escribes genial! ✏️',3,()=>initG12(cont,window.ppGetLevel()),_lv);}
						else nextLetter();
					},600);
				}
			}
		}

		function nextLetter(){
			if(round>=data.length){const _lv=window.ppWin();window.ppCelebrate('¡Escribes genial! ✏️',3,()=>initG12(cont,window.ppGetLevel()),_lv);return;}
			setPbar(round,data.length);
			const letter=data[round];
			const el=/** @type {HTMLElement} */ (cont.querySelector('#g12letter'));el.textContent='Traza: '+letter;
			const cvs=/** @type {HTMLCanvasElement} */ (cont.querySelector('#g12cvs')), wrap=/** @type {HTMLElement} */ (cvs.parentElement);
			const W=Math.min(wrap.clientWidth-16,350), H=Math.min(window.innerHeight-300,300);
			cvs.width=W;cvs.height=H;ctx=cvs.getContext('2d');
			const def=/** @type {Record<string,number[][]>} */ (G12_PATHS)[letter];
			if(!def){round++;nextLetter();return;}
			curPts=def.map((/** @type {number[]} */ p)=>[p[0]*W/100,p[1]*H/100]);
			ptIdx=0;
			const drawBg=()=>{
				const c = ctx;
				if(!c) return;
				c.fillStyle='#F5F5F5';c.fillRect(0,0,W,H);
				c.font=`bold ${H*.75}px Nunito,sans-serif`;c.fillStyle='#DEDEDE';c.textAlign='center';c.textBaseline='middle';
				c.fillText(letter,W/2,H/2);drawDots();
			};
			if(document.fonts&&document.fonts.ready)document.fonts.ready.then(drawBg);else setTimeout(drawBg,100);
			cvs.ontouchstart=e=>{e.preventDefault();handleTouch(e.touches[0],cvs);};
			cvs.ontouchmove=e=>{e.preventDefault();handleTouch(e.touches[0],cvs);};
			cvs.onmousedown=e=>handleTouch(e,cvs);
			cvs.onmousemove=e=>{if(e.buttons)handleTouch(e,cvs);};
			window.ppSay('Traza la letra '+letter);
		}
		window.ppSay('¡Toca los puntos en orden para escribir la letra!');
		nextLetter();
	}
</script>

<GameShell gameNum={12} title="Traza Letras" icon="✏️" initGame={initG12} />
