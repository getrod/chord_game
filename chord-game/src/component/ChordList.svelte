<script>
    import { flip } from 'svelte/animate';
    export let chords
</script>

<style>
	.chord-sequence {
        display: flex;
		flex-direction: row;
        flex-wrap: wrap;
	}
    
    .chord-text {
		text-align: center;
		padding: 0 10px 0 10px;
	}
</style>

<div class="chord-sequence">
    {#each chords as chord, i (chord.id)}
        <div animate:flip class="chord-card" style={i === 0 ? 'background-color: green;' : ''}>
            <p class="chord-text" style={i === 0 ? 'color: white;' : ''}>
                {chord.data.keyName + chord.data.chordName}
            </p>
        </div>
    {/each}
</div>