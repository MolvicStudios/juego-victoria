<script>
	import { onDestroy } from 'svelte';
	import GameShell from '$lib/components/GameShell.svelte';
	import { lerpParam } from '$lib/data.js';

	const COLS = ['#FF6B6B','#FF9F43','#FFD93D','#6BCB77','#4D9FEC','#A78BFA','#F472B6','#2DD4BF'];
	const EMOJIS = ['🎈','🎈','🎈','🎈','🌟','💖','🌸','⭐','🍭','🎊'];

	let container, g17Popped = 0, g17Total = 0, g17Lv = 1, g17TimerId = null;

	function initG17(cont, lv) {
		container = cont;
		g17Lv = lv;
		g17Popped = 0;
		g17Total = lerpParam(lv, 8, 25);

		container.innerHTML = `
			<div class="pbar"><div class="pfill" id="g17pb" style="width:0%;background:#F472B6"></div></div>
			<div class="ins">¡Toca los globos para reventarlos! 🎈</div>
			<div class="g17-arena" id="g17a"></div>
			<div class="g17-count" id="g17c">${g17Total} globos quedan</div>`;

		showBalloon();
		window.ppSay('¡Toca los globos!');
	}

	function showBalloon() {
		const arena = container?.querySelector('#g17a');
		if (!arena) return;
		arena.innerHTML = '';

		const size = lerpParam(g17Lv, 110, 50);
		const col = COLS[Math.floor(Math.random() * COLS.length)];
		const emoji = EMOJIS[Math.floor(Math.random() * (g17Lv >= 8 ? EMOJIS.length : 4))];
		const left = 5 + Math.random() * (80 - (size / 5));
		const top  = 5 + Math.random() * 55;

		const el = document.createElement('div');
		el.style.cssText = `
			position:absolute;width:${size}px;height:${size}px;border-radius:50%;background:${col};
			left:${left}%;top:${top}%;font-size:${Math.round(size * 0.55)}px;
			display:flex;align-items:center;justify-content:center;cursor:pointer;
			box-shadow:0 6px 20px rgba(0,0,0,.18);animation:popIn .25s;
			user-select:none;-webkit-tap-highlight-color:transparent;
			transition:transform .18s,opacity .18s`;
		el.textContent = emoji;

		/* Auto-disappear at level ≥ 8 creating time pressure */
		const autoMs = lerpParam(g17Lv, 5000, 1600);
		if (g17Lv >= 8) {
			g17TimerId = setTimeout(() => {
				if (el.parentNode) {
					el.style.opacity = '0';
					setTimeout(() => { if (el.parentNode) { el.remove(); showBalloon(); } }, 200);
				}
			}, autoMs);
		}

		function pop(e) {
			e.preventDefault();
			if (!el.parentNode) return;
			if (g17TimerId) { clearTimeout(g17TimerId); g17TimerId = null; }
			el.style.transform = 'scale(2)';
			el.style.opacity = '0';
			el.style.pointerEvents = 'none';
			window.ppBeep(500 + Math.random() * 400, 0.18);
			window.ppOnCorrect();
			g17Popped++;
			const pb = container?.querySelector('#g17pb');
			const ct = container?.querySelector('#g17c');
			if (pb) pb.style.width = (g17Popped / g17Total * 100) + '%';
			if (ct) ct.textContent = (g17Total - g17Popped) + ' globos quedan';
			if (g17Popped >= g17Total) {
				setTimeout(() => {
					const _lv = window.ppWin();
					window.ppCelebrate('¡Reventaste todos los globos! 🎈', 3, () => initG17(container, window.ppGetLevel()), _lv);
				}, 500);
			} else {
				setTimeout(showBalloon, 350);
			}
		}

		el.addEventListener('click', pop);
		el.addEventListener('touchstart', pop, { passive: false });
		arena.appendChild(el);
	}

	onDestroy(() => { if (g17TimerId) clearTimeout(g17TimerId); });

	function initContainer(cont, lv) { initG17(cont, lv); }
</script>

<GameShell gameNum={17} title="Globos" icon="🎈" initGame={initContainer} />
