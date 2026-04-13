<script>
	import { particleGroups } from '$lib/effects/particleEvents.js';
	import { quietMode } from '$lib/stores/accessibility.js';

	let isQuiet = $state(false);
	quietMode.subscribe(v => { isQuiet = v; });

	let groups = $state([]);
	particleGroups.subscribe(v => { groups = v; });

	function starClip() {
		const pts = [];
		for (let i = 0; i < 10; i++) {
			const r = i % 2 === 0 ? 50 : 20;
			const a = (i * 36 - 90) * (Math.PI / 180);
			pts.push(`${50 + r * Math.cos(a)}% ${50 + r * Math.sin(a)}%`);
		}
		return `polygon(${pts.join(',')})`;
	}

	const STAR_CLIP = starClip();
</script>

{#each groups as group (group.id)}
	{#each group.items as p (p.id)}
		{@const style = [
			`position:fixed`,
			`left:${p.x}px`,
			`top:${p.y}px`,
			`width:${p.size}px`,
			`height:${p.size}px`,
			`background:${p.color}`,
			`border-radius:${p.type === 'circle' ? '50%' : p.type === 'rect' ? '2px' : '0'}`,
			`clip-path:${p.type === 'star' ? STAR_CLIP : 'none'}`,
			`pointer-events:none`,
			`z-index:9999`,
			`animation:pp-particle-fly ${p.dur}ms cubic-bezier(0.22,1,0.36,1) ${p.delay || 0}ms both`,
			`--dx:${p.dx}px`,
			`--dy:${p.dy}px`,
			`--rot:${p.rotate || Math.random() * 360}deg`,
			`--gravity:${p.gravity ? 1 : 0}`,
		].join(';')}
		<div {style}></div>
	{/each}
{/each}

<style>
	/* Las partículas usan CSS custom properties para su trayectoria.
	   Se montan con position:fixed y pointer-events:none para no interferir. */
	@keyframes -global-pp-particle-fly {
		0%   { opacity: 1;  transform: translate(0, 0) rotate(0deg) scale(1); }
		70%  { opacity: 0.9; }
		100% {
			opacity: 0;
			transform:
				translate(var(--dx), calc(var(--dy) + var(--gravity, 0) * 40px))
				rotate(var(--rot))
				scale(0.5);
		}
	}
</style>
