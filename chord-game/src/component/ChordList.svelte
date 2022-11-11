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
    {#each chords as chord, i (chord)}
        <div animate:flip class="chord-card" style={i === 0 ? 'background-color: green;' : ''}>
            {#if chord.type === 'BrokenChord'}
                <p class="chord-text" style={i === 0 ? 'color: white;' : ''}>
                    {chord.keyName + chord.chordName + ': ' + chord.sequence}
                </p>  
            {:else}
                <p class="chord-text" style={i === 0 ? 'color: white;' : ''}>
                    {chord.keyName + chord.chordName}
                </p>  
            {/if}
            
           
        </div>
    {/each}
</div>