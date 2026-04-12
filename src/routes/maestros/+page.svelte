<script>
	import WorldHub from '$lib/components/WorldHub.svelte';
	// Maestros: 9-12 años — juegos más difíciles, sin juegos de bebé ni fáciles
	const GAME_NUMS = [2, 3, 6, 7, 8, 11, 12, 13, 14, 15, 16];
</script>

<WorldHub
	worldId="maestros"
	worldEmoji="🏆"
	worldLabel="Maestros"
	worldColor="#FF9F43"
	gameNums={GAME_NUMS}
/>
