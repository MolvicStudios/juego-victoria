<script>
	import WorldHub from '$lib/components/WorldHub.svelte';
	// Maestros: 9-12 años — 15 juegos más desafiantes (sin juegos de bebé ni dibujo libre)
	const GAME_NUMS = [11, 16, 14, 12, 3, 8, 7, 13, 2, 15, 9, 5, 6, 1, 10];
</script>

<WorldHub
	worldId="maestros"
	worldEmoji="🏆"
	worldLabel="Maestros"
	worldColor="#FF9F43"
	gameNums={GAME_NUMS}
/>
