<script>
	import WorldHub from '$lib/components/WorldHub.svelte';
	// Aventureros: 6-8 años — juegos con mayor reto, sin juegos de bebé
	const GAME_NUMS = [2, 3, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16];
</script>

<WorldHub
	worldId="aventureros"
	worldEmoji="⚔️"
	worldLabel="Aventureros"
	worldColor="#6BCB77"
	gameNums={GAME_NUMS}
/>
