<script>
    import ChordSequence from '../component/ChordSequence.svelte'
    import { chordGeneratorRandom } from '../lib/ChordSequence.svelte'
    import { getChordProgression, addKeysToChordSequence } from '../lib/ChordProression.svelte'
    import { chordMatch } from '../lib/Chord.svelte'
    import ActiveNotes from '../lib/ActiveNotes.svelte'

    $: chordSequence = []
    let sequenceIndex = 0
    let notes = []
    let chordProgStr = "[1]-maj [4]-maj [5]-maj"
    let keysStr = "0"

    function handleClick(e) {
        sequenceIndex = 0
        chordSequence = []
        let keys = keysStr.split(',')
        console.log(keys)
        keys.forEach((key) => {
            let chords = getChordProgression(chordProgStr, parseInt(key))
            chordSequence = chordSequence.concat(chords)
            console.log(chordSequence)
        })
        
    }

    function handleNoteEvent(e) {
        if (chordSequence.length == 0 || sequenceIndex >= chordSequence.length) return
        notes = e.detail.activeNotes
        if (chordMatch(notes, chordSequence[sequenceIndex].name)) {
            sequenceIndex++
        }
    }

</script>


<ActiveNotes on:note={handleNoteEvent}/>
<h1>Chord Progression</h1>
<ChordSequence chordSequence={addKeysToChordSequence(chordSequence)} {sequenceIndex}/>

<form class="content">
    <label for='prog'>Progression Formula</label>
    <input type="text" bind:value={chordProgStr} placeholder="ex: [1]-maj [4]-maj [5]-maj"/>
    <label for='prog'>Keys</label>
    <input type="text" bind:value={keysStr} placeholder="ex: 0 for key 'C'"/>
  </form>
<button on:click={handleClick}>Play</button>

<style>
    .content {
      display: grid;
      grid-column-gap: 10px;
      padding: 0% 20% 0% 0%;
    }
</style>