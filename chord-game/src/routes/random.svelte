<script>
    import ChordSequence from '../component/ChordSequence.svelte'
    import { chordGeneratorRandom } from '../lib/ChordSequence.svelte'
    import { getChordProgression, addKeysToChordSequence } from '../lib/ChordProression.svelte'
    import { chordMatch, noteName } from '../lib/Chord.svelte'
    import ActiveNotes from '../lib/ActiveNotes.svelte'

    $: chordSequence = chordGeneratorRandom(12)
    let sequenceIndex = 0
    let notes = []
    let chordFilterStr = ""
    let keyFilterStr = ""
    let lengthStr = "10"
    let gameStart = false

    function handlePlayGame() {
        let chordFilter = chordFilterStr.replace(/\s+/g, '').split(',')
        let keyFilter = keyFilterStr.replace(/\s+/g, '').split(',')
        keyFilter.forEach((key, index) => keyFilter[index] = noteName(key))

        if (chordFilterStr.trim() === "") chordFilter = null
        if (keyFilterStr.trim() === "") keyFilter = null
        let length = parseInt(lengthStr)
        if (isNaN(length)) {
            length = 10
        }

        chordSequence = chordGeneratorRandom(length, keyFilter, chordFilter)
        sequenceIndex = 0
        gameStart = true
    }

    function handleNewGame() {
        gameStart = false
    }

    function handleNoteEvent(e) {
        // if sequence over, no checking
        if (chordSequence.length == 0 || sequenceIndex >= chordSequence.length) return

        notes = e.detail.activeNotes
        if (chordMatch(notes, chordSequence[sequenceIndex].name)) {
            sequenceIndex++
        }
    }

</script>

{#if gameStart}
    <h1>Random Chord</h1>
    <ActiveNotes on:note={handleNoteEvent}/>
    <ChordSequence chordSequence={addKeysToChordSequence(chordSequence)} {sequenceIndex}/>
    <button on:click={handleNewGame}> New Game </button>
{:else}
    <h2>Filters</h2> 
    <p>Leave empty to play all defined chords</p>
    <form class="content">
        <label for='prog'>Chord Filter</label>
        <input type="text" bind:value={chordFilterStr} placeholder="ex: maj, m, m9, etc."/>
        <label for='prog'>Key Filter</label>
        <input type="text" bind:value={keyFilterStr} placeholder="ex: 0, 2, 5 for 'C, D, F'"/>
        <label for='prog'>Length</label>
        <input type="text" bind:value={lengthStr}/>
    </form>
    <button on:click={handlePlayGame}> Play Game </button>
{/if}
<style>
    .content {
      display: grid;
      grid-column-gap: 10px;
      padding: 0% 20% 0% 0%;
    }
</style>