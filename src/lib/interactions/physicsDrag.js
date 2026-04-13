/**
 * PhysicsDrag — Directiva Svelte para drag-and-drop con física.
 *
 * Usa única y exclusivamente Pointer Events API (touch + mouse + stylus).
 * El drag es una mejora progresiva; el click/tap sigue funcionando.
 *
 * Uso:
 *   <div use:physicsDrag={{ targets: '.drop-zone', onCorrect, onWrong }}>
 *
 * El callback onCorrect/onWrong recibe el elemento target que coincidió (o null).
 *
 * @param {HTMLElement} node - El elemento arrastrable
 * @param {{ targets: string, onCorrect: (target: HTMLElement) => void, onWrong: (target: HTMLElement|null) => void }} options
 */
export function physicsDrag(node, options) {
	let { targets, onCorrect, onWrong } = options;

	// Estado de la animación de seguimiento
	let isDragging = false;
	/** @type {HTMLElement|null} */
	let clone = null;
	/** @type {HTMLElement|null} */
	let ghost = null;
	let targetX = 0, targetY = 0;
	let currentX = 0, currentY = 0;
	let startX = 0, startY = 0;
	let rafId = 0;
	let pointerId = -1;
	// Guardar tamaño del nodo original
	let nodeW = 0, nodeH = 0;

	function onPointerDown(/** @type {PointerEvent} */ e) {
		// Solo disparar con botón primario (mouse izq / primer toque)
		if (e.button && e.button !== 0) return;
		e.preventDefault();

		const rect = node.getBoundingClientRect();
		nodeW = rect.width; nodeH = rect.height;

		startX = e.clientX; startY = e.clientY;
		targetX = currentX = e.clientX - nodeW / 2;
		targetY = currentY = e.clientY - nodeH / 2;
		pointerId = e.pointerId;

		// Capturar el puntero para no perder el drag al salir del elemento
		try { node.setPointerCapture(e.pointerId); } catch {}

		// Crear un clon visual que seguirá al cursor con lag
		clone = /** @type {HTMLElement} */ (node.cloneNode(true));
		clone.style.cssText = [
			'position:fixed',
			`left:${currentX}px`,
			`top:${currentY}px`,
			`width:${nodeW}px`,
			`height:${nodeH}px`,
			'pointer-events:none',
			'z-index:9998',
			'transition:box-shadow 150ms,transform 150ms',
			'box-shadow:0 16px 32px rgba(0,0,0,0.22)',
			'transform:scale(1.1)',
			'cursor:grabbing',
		].join(';');
		document.body.appendChild(clone);

		// Crear ghost semitransparente en posición original
		ghost = node;
		ghost.style.opacity = '0.3';
		ghost.style.pointerEvents = 'none';

		isDragging = true;
		rafLoop();
	}

	function onPointerMove(/** @type {PointerEvent} */ e) {
		if (!isDragging || e.pointerId !== pointerId) return;
		targetX = e.clientX - nodeW / 2;
		targetY = e.clientY - nodeH / 2;
	}

	function onPointerUp(/** @type {PointerEvent} */ e) {
		if (!isDragging || e.pointerId !== pointerId) return;
		isDragging = false;
		cancelAnimationFrame(rafId);

		if (!clone || !ghost) return;

		// Ocultar el clone temporalmente para poder usar elementFromPoint
		clone.style.visibility = 'hidden';
		const under = document.elementFromPoint(e.clientX, e.clientY);
		clone.style.visibility = '';

		// Buscar si hay un drop-zone válido bajo el cursor
		/** @type {HTMLElement|null} */
		const dropTarget = under ? /** @type {HTMLElement|null} */ (under.closest(targets)) : null;

		if (dropTarget && isValidDrop(node, dropTarget)) {
			// ACIERTO: snap magnético al destino
			const dRect = dropTarget.getBoundingClientRect();
			clone.style.transition = 'transform 200ms cubic-bezier(0.34,1.56,0.64,1), left 200ms cubic-bezier(0.34,1.56,0.64,1), top 200ms cubic-bezier(0.34,1.56,0.64,1)';
			clone.style.left = dRect.left + 'px';
			clone.style.top  = dRect.top  + 'px';
			clone.style.transform = 'scale(1)';
			clone.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
			setTimeout(() => {
				clone?.remove(); clone = null;
				if (ghost) { ghost.style.opacity = ''; ghost.style.pointerEvents = ''; ghost = null; }
			}, 220);
			onCorrect?.(dropTarget);
		} else {
			// FALLO: vuela de vuelta al origen
			const rect = node.getBoundingClientRect();
			const dx = Math.abs(currentX - (rect.left));
			const dy = Math.abs(currentY - (rect.top));
			const dist = Math.sqrt(dx * dx + dy * dy);
			const returnDur = Math.min(600, 150 + dist * 0.8);
			clone.style.transition = `left ${returnDur}ms cubic-bezier(0.22,1,0.36,1), top ${returnDur}ms cubic-bezier(0.22,1,0.36,1), transform ${returnDur + 100}ms, box-shadow ${returnDur}ms`;
			clone.style.left = rect.left + 'px';
			clone.style.top  = rect.top  + 'px';
			clone.style.transform = 'scale(1)';
			clone.style.boxShadow = '0 2px 4px rgba(0,0,0,0.12)';
			setTimeout(() => {
				// Pequeño rebote al llegar
				if (clone) { clone.style.transition = 'transform 200ms cubic-bezier(0.34,1.56,0.64,1)'; clone.style.transform = 'scale(1.15)'; }
				setTimeout(() => {
					if (clone) { clone.style.transform = 'scale(1)'; }
					setTimeout(() => {
						clone?.remove(); clone = null;
						if (ghost) { ghost.style.opacity = ''; ghost.style.pointerEvents = ''; ghost = null; }
					}, 200);
				}, 200);
			}, returnDur);
			onWrong?.(dropTarget);
		}

		try { node.releasePointerCapture(e.pointerId); } catch {}
	}

	/**
	 * Comprueba si el nodo arrastrado es compatible con el drop-zone.
	 * Estrategia: compara data-id de ambos elementos (convención de los juegos existentes).
	 * @param {HTMLElement} src
	 * @param {HTMLElement} dst
	 */
	function isValidDrop(src, dst) {
		if (src.dataset.id && dst.dataset.id) {
			return src.dataset.id === dst.dataset.id;
		}
		// Fallback: cualquier drop-zone es válido (el juego decide)
		return true;
	}

	/** Loop de interpolación de posición (sensación de peso/inercia) */
	function rafLoop() {
		if (!isDragging || !clone) return;
		// Lerp con factor 0.2 → lag suave tipo inercia
		currentX += (targetX - currentX) * 0.22;
		currentY += (targetY - currentY) * 0.22;
		clone.style.left = currentX + 'px';
		clone.style.top  = currentY + 'px';
		rafId = requestAnimationFrame(rafLoop);
	}

	node.style.cursor = 'grab';
	node.addEventListener('pointerdown', onPointerDown, { passive: false });
	node.addEventListener('pointermove', onPointerMove, { passive: true });
	node.addEventListener('pointerup',   onPointerUp);
	node.addEventListener('pointercancel', onPointerUp);

	return {
		/** Actualiza las opciones (targets, callbacks) en caliente */
		update(newOpts) {
			targets     = newOpts.targets;
			onCorrect   = newOpts.onCorrect;
			onWrong     = newOpts.onWrong;
		},
		destroy() {
			cancelAnimationFrame(rafId);
			clone?.remove();
			if (ghost) { ghost.style.opacity = ''; ghost.style.pointerEvents = ''; }
			node.removeEventListener('pointerdown', onPointerDown);
			node.removeEventListener('pointermove', onPointerMove);
			node.removeEventListener('pointerup',   onPointerUp);
			node.removeEventListener('pointercancel', onPointerUp);
		},
	};
}
