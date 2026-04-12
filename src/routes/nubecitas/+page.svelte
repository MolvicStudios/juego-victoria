<script>
	import WorldHub from '$lib/components/WorldHub.svelte';
	// Nubecitas: 0-2 años — juegos visuales y táctiles (sin aritmética, sin laberinto, sin traza)
	const GAME_NUMS = [1, 4, 6, 10, 5, 8, 9, 17, 18, 2, 3, 7, 13, 15, 16, 22, 29, 30, 34, 36, 37];
</script>

<WorldHub
	worldId="nubecitas"
	worldEmoji="☁️"
	worldLabel="Nubecitas"
	worldColor="#A78BFA"
	gameNums={GAME_NUMS}
/>
