<script>
	import WorldHub from '$lib/components/WorldHub.svelte';
	// Aventureros: 6-8 años — juegos con laberinto y mayor reto cognitivo
	const GAME_NUMS = [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 19, 20, 21, 23, 24, 25, 26, 27, 29, 31, 32, 34, 35, 36, 38];
</script>

<WorldHub
	worldId="aventureros"
	worldEmoji="⚔️"
	worldLabel="Aventureros"
	worldColor="#6BCB77"
	gameNums={GAME_NUMS}
/>
