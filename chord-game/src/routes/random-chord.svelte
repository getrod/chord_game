<script>
    import {chordGeneratorRandom} from '../lib/ChordSequence.svelte'
    import {chordInterpreter} from '../lib/Chord.svelte'
    import ActiveNotes from '../lib/ActiveNotes.svelte'

    $: chordSequence = []
    let notes = []
    let sequenceIndex = 0

    function handleClick() {
        chordSequence = chordGeneratorRandom(7)
        chordSequence.forEach((chord, index) => chordSequence[index] = {id: index, name: chord})
        sequenceIndex = 0
    }

    function handleNoteEvent(e) {
        notes = e.detail.activeNotes
        let chordNames = chordInterpreter(notes)
        let match = false
        if (chordSequence.length == 0 || sequenceIndex >= chordSequence.length) return
        console.log(chordNames + ' ' + chordSequence[sequenceIndex].name)
        chordNames.forEach((chordName) => {
            if (chordName === chordSequence[sequenceIndex].name) {
                match = true
                sequenceIndex++
            }
        })
    } 
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

<h1>Random Chord</h1>
<ActiveNotes on:note={handleNoteEvent}/>
<div class="chord-sequence">
{#each chordSequence as chord (chord.id)}
    {#if chord.id < sequenceIndex}
        <p style="color: #a6a4a4;">{chord.name}</p>
    {:else if chord.id === sequenceIndex}
        <p style="color: green;">{chord.name}</p>
    {:else}
        <p>{chord.name}</p>
    {/if}
    
{/each}
</div>
<button on:click={handleClick}> New Game </button>