<script>
	import { onMount, onDestroy } from 'svelte';
	import GameShell from '$lib/components/GameShell.svelte';
	import { shuf, lerpParam } from '$lib/data.js';

	/** @type {(key: string, vars?: Record<string, string|number>) => string} */ const T = (key, vars) => window.ppT?.(key, vars) ?? key;

	const G1_SHAPES = [
		{id:'ci',l:'games.g1.shapes.circle',e:'⭕',bg:'#FF6B6B'},
		{id:'sq',l:'games.g1.shapes.square',e:'🟧',bg:'#FF9F43'},
		{id:'tr',l:'games.g1.shapes.triangle',e:'🔺',bg:'#4D9FEC'},
		{id:'st',l:'games.g1.shapes.star',e:'⭐',bg:'#FFD93D'},
		{id:'he',l:'games.g1.shapes.heart',e:'❤️',bg:'#F472B6'},
		{id:'mo',l:'games.g1.shapes.moon',e:'🌙',bg:'#A78BFA'},
		{id:'di',l:'games.g1.shapes.diamond',e:'💎',bg:'#2DD4BF'},
		{id:'fl',l:'games.g1.shapes.flower',e:'🌸',bg:'#6BCB77'},
	];

	/** @type {HTMLDivElement|null} */
	let container = $state(null);
	/** @type {HTMLDivElement|null} */
	let g1Ghost = null;
	/** @type {HTMLDivElement|null} */
	let g1DragEl = null;
	let g1Matched = 0;
	/** @type {HTMLDivElement|null} */
	let g1TapSel = null;
	let g1TouchMoved = false, g1MouseMoved = false;

	/** @param {HTMLDivElement} cont @param {number} lv */
	function initG1(cont, lv) {
		container = cont;
		if (!container) return;
		cleanup();
		g1Matched = 0; g1TapSel = null;
		const count = lv<=3?lerpParam(lv,3,4):lv<=6?lerpParam(lv-3,4,5):lv<=9?lerpParam(lv-6,5,6):lv<=12?lerpParam(lv-9,6,7):8;
		const sel = shuf(G1_SHAPES).slice(0, Math.min(count, G1_SHAPES.length));
		const showLabel = lv <= 3;
		const useRotation = lv >= 7;

		container.innerHTML = `
			<div class="ins">${T('games.g1.instruction')}</div>
			<div class="g1-shapes" id="g1shapes"></div>
			<div style="font-size:.72rem;font-weight:700;color:var(--ink2)">${T('games.g1.siluetas')}</div>
			<div class="g1-outlines" id="g1outs"></div>`;

		const shapesEl = /** @type {HTMLDivElement} */ (container.querySelector('#g1shapes'));
		const outsEl = /** @type {HTMLDivElement} */ (container.querySelector('#g1outs'));

		sel.forEach(s => {
			const el = document.createElement('div'); el.className = 'g1-shape'; el.dataset.id = s.id;
			el.style.background = s.bg; el.textContent = s.e;
			if (useRotation) el.style.transform = 'rotate(' + Math.floor(Math.random()*4)*90 + 'deg)';
			el.addEventListener('touchstart', e => { e.preventDefault(); g1TouchMoved = false; g1StartDrag(e, el, s); }, {passive:false});
			el.addEventListener('touchend', e => {
				e.preventDefault();
				if (!g1TouchMoved) { if(g1Ghost){g1Ghost.remove();g1Ghost=null;if(g1DragEl){g1DragEl.style.opacity='1';g1DragEl=null;}} g1TapSelect(el,s); return; }
				const t = e.changedTouches[0]; g1FinishDrag(t.clientX, t.clientY);
			});
			el.addEventListener('mousedown', e => g1StartDragMouse(e, el, s));
			el.onclick = () => { if(!g1Ghost) g1TapSelect(el, s); };
			shapesEl.appendChild(el);
		});

		const outOrder = lv>=13 ? shuf([...sel]) : shuf(sel);
		outOrder.forEach(s => {
			const el = document.createElement('div'); el.className = 'g1-out'; el.dataset.id = s.id;
			if (showLabel) el.innerHTML = '<span>'+s.e+'</span><p>'+T(s.l)+'</p>';
			else if (lv<=9) el.innerHTML = '<span>'+s.e+'</span>';
			else el.innerHTML = '<span style="opacity:.15">'+s.e+'</span>';
			el.addEventListener('touchend', e => { e.preventDefault(); if(g1TapSel) g1TapPlace(el); });
			el.onclick = () => { if(g1TapSel) g1TapPlace(el); };
			outsEl.appendChild(el);
		});

		document.addEventListener('touchmove', g1MoveDrag, {passive:false});
		document.addEventListener('touchend', g1EndDrag);
		document.addEventListener('mousemove', g1MoveMouseDrag);
		document.addEventListener('mouseup', g1EndMouseDrag);
		window.ppSay(T('games.g1.hello'));
	}

	/** @param {TouchEvent} e @param {HTMLDivElement} el @param {{id:string,l:string,e:string,bg:string}} shape */
	function g1StartDrag(e, el, shape) {
		const t = e.touches[0], r = el.getBoundingClientRect();
		g1DragEl = el;
		g1Ghost = document.createElement('div'); g1Ghost.className = 'g1-ghost';
		g1Ghost.style.cssText = `width:${r.width}px;height:${r.height}px;background:${shape.bg};left:${t.clientX-r.width/2}px;top:${t.clientY-r.height/2}px`;
		g1Ghost.textContent = shape.e; document.body.appendChild(g1Ghost); el.style.opacity = '.2'; window.ppBeep(600,.1);
	}
	/** @param {MouseEvent} e @param {HTMLDivElement} el @param {{id:string,l:string,e:string,bg:string}} shape */
	function g1StartDragMouse(e, el, shape) {
		g1MouseMoved = false;
		const r = el.getBoundingClientRect(); g1DragEl = el;
		g1Ghost = document.createElement('div'); g1Ghost.className = 'g1-ghost';
		g1Ghost.style.cssText = `width:${r.width}px;height:${r.height}px;background:${shape.bg};left:${e.clientX-r.width/2}px;top:${e.clientY-r.height/2}px`;
		g1Ghost.textContent = shape.e; document.body.appendChild(g1Ghost); el.style.opacity = '.2'; window.ppBeep(600,.1);
	}
	/** @param {TouchEvent} e */
	function g1MoveDrag(e) { if(!g1Ghost) return; e.preventDefault(); g1TouchMoved = true; const t = e.touches[0]; g1Ghost.style.left = (t.clientX-g1Ghost.offsetWidth/2)+'px'; g1Ghost.style.top = (t.clientY-g1Ghost.offsetHeight/2)+'px'; }
	/** @param {MouseEvent} e */
	function g1MoveMouseDrag(e) { if(!g1Ghost) return; g1MouseMoved = true; g1Ghost.style.left = (e.clientX-g1Ghost.offsetWidth/2)+'px'; g1Ghost.style.top = (e.clientY-g1Ghost.offsetHeight/2)+'px'; }
	/** @param {number} cx @param {number} cy */
	function g1FinishDrag(cx, cy) {
		if (!g1Ghost || !g1DragEl) return;
		g1Ghost.style.visibility = 'hidden';
		const under = document.elementFromPoint(cx, cy);
		g1Ghost.remove(); g1Ghost = null;
		const target = /** @type {HTMLElement|null} */ (under?.closest('.g1-out'));
		if (target && g1DragEl && target.dataset.id === g1DragEl.dataset.id) {
			target.classList.add('ok'); g1DragEl.classList.add('used'); g1DragEl.style.opacity = '';
			const sayKey = G1_SHAPES.find(s => s.id === g1DragEl?.dataset.id)?.l || '';
			window.ppBeep(880,.2); window.ppSay(T('games.common.correct_name', {name: T(sayKey)}));
			window.ppOnCorrect(); g1Matched++;
			if (container && g1Matched === container.querySelectorAll('.g1-shape').length) {
				const _lv = window.ppWin(); cleanup(); setTimeout(() => window.ppCelebrate(T('games.g1.win')+' 🔷', 3, () => { if(container) initG1(container, window.ppGetLevel()); }, _lv), 400);
			}
		} else {
			g1DragEl.style.opacity = '1'; g1DragEl.classList.add('err');
			setTimeout(() => g1DragEl?.classList.remove('err'), 400); window.ppOnWrong(); window.ppBoo();
		}
		g1DragEl = null;
	}
	/** @param {TouchEvent} e */
	function g1EndDrag(e) {
		if (!g1Ghost) return;
		const t = e.changedTouches[0];
		if (!g1TouchMoved) { g1Ghost.remove(); g1Ghost = null; if(g1DragEl){const el=g1DragEl;el.style.opacity='1';g1DragEl=null;const shape=G1_SHAPES.find(s=>s.id===el.dataset.id);if(shape)g1TapSelect(el,shape);} return; }
		g1FinishDrag(t.clientX, t.clientY);
	}
	/** @param {MouseEvent} e */
	function g1EndMouseDrag(e) { if (!g1Ghost) return; if (!g1MouseMoved) { g1Ghost.remove(); g1Ghost = null; if(g1DragEl){g1DragEl.style.opacity='1';g1DragEl=null;} return; } g1FinishDrag(e.clientX, e.clientY); }

	/** @param {HTMLDivElement} el @param {{id:string,l:string,e:string,bg:string}} shape */
	function g1TapSelect(el, shape) {
		if (!el || el.classList.contains('used')) return;
		const already = g1TapSel === el;
		container?.querySelectorAll('.g1-shape').forEach(x => { const h = /** @type {HTMLElement} */ (x); h.style.outline = ''; h.style.boxShadow = ''; });
		if (already) { g1TapSel = null; return; }
		g1TapSel = el; el.style.outline = '4px solid var(--c3)'; el.style.boxShadow = '0 0 0 6px rgba(255,217,61,.4)';
		window.ppBeep(600,.12); window.ppSay(T('games.common.where_name', {name: T(shape.l)}));
	}
	/** @param {HTMLDivElement} outEl */
	function g1TapPlace(outEl) {
		if (!g1TapSel) return;
		const selId = g1TapSel.dataset.id;
		if (outEl.dataset.id === selId) {
			outEl.classList.add('ok');
			const sayKey = G1_SHAPES.find(s => s.id === selId)?.l || '';
			g1TapSel.classList.add('used'); g1TapSel.style.outline = ''; g1TapSel.style.boxShadow = ''; g1TapSel = null;
			window.ppBeep(880,.22); window.ppSay(T('games.common.correct_name', {name: T(sayKey)}));
			window.ppOnCorrect(); g1Matched++;
			if (container && g1Matched === container.querySelectorAll('.g1-shape').length) {
				const _lv = window.ppWin(); cleanup(); setTimeout(() => window.ppCelebrate(T('games.g1.win')+' 🔷', 3, () => { if(container) initG1(container, window.ppGetLevel()); }, _lv), 400);
			}
		} else {
			outEl.classList.add('err'); setTimeout(() => outEl.classList.remove('err'), 400);
			g1TapSel.style.outline = ''; g1TapSel.style.boxShadow = ''; g1TapSel = null;
			window.ppOnWrong(); window.ppBoo(); window.ppSay(T('games.common.not_there'));
		}
	}

	function cleanup() {
		document.removeEventListener('touchmove', g1MoveDrag);
		document.removeEventListener('touchend', g1EndDrag);
		document.removeEventListener('mousemove', g1MoveMouseDrag);
		document.removeEventListener('mouseup', g1EndMouseDrag);
		if (g1Ghost) { g1Ghost.remove(); g1Ghost = null; }
		g1TapSel = null;
	}

	onDestroy(cleanup);
</script>

<GameShell gameNum={1} title="Puzle de Formas" icon="🔷" initGame={initG1} />
