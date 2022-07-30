<script>
    import { onMount } from "svelte";


    export let chordSequence = []
    export let sequenceIndex = 0

    onMount(() => {
        // should use typescript
        sequenceIndex = parseInt(sequenceIndex)
    })
</script>

<style>
	.chord-sequence {
        display: flex;
		flex-direction: row;
        flex-wrap: wrap;
	}
    
    p {
        margin: 20px;
    }
</style>

<div class="chord-sequence">
{#each chordSequence as chord (chord.id)}
    {#if chord.id < sequenceIndex}
        <p style="color: #a6a4a4;">{chord.name}</p>
    {:else if chord.id == sequenceIndex}
        <p style="color: green;">{chord.name}</p>
    {:else}
        <p>{chord.name}</p>
    {/if}
{/each}
</div>