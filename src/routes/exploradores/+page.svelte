<script>
	import WorldHub from '$lib/components/WorldHub.svelte';
	// Exploradores: 3-5 años — 15 juegos educativos base (sin laberinto, sin juegos bebé)
	const GAME_NUMS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16];
</script>

<WorldHub
	worldId="exploradores"
	worldEmoji="🌏"
	worldLabel="Exploradores"
	worldColor="#4D9FEC"
	gameNums={GAME_NUMS}
/>
