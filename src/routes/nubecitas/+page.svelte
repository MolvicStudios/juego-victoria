<script>
	import WorldHub from '$lib/components/WorldHub.svelte';
	// Nubecitas: 0-2 años — juegos sensoriales muy simples
	// Formas(1), Pintar(4), Colores(10), Piano(6), Memoria(5) — los más visuales y táctiles
	const GAME_NUMS = [1, 4, 5, 6, 10];
</script>

<WorldHub
	worldId="nubecitas"
	worldEmoji="☁️"
	worldLabel="Nubecitas"
	worldColor="#A78BFA"
	gameNums={GAME_NUMS}
/>
