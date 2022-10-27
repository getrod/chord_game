<script>
	import { onMount } from "svelte";
    import ChordSequence from "../component/ChordSequence.svelte";
	import { chordGeneratorRandom } from "../lib/ChordSequence.svelte"; //TODO: DEBUG!!!!
    import MidiListener from "../lib/MidiListener.svelte";
	import { addKeysToArray, MIDI_MESSAGE } from "../lib/Util.svelte";

    let notes = new Set();
    let chordSequence = [];

    onMount(() => {
        chordSequence = chordGeneratorRandom(6);
        addKeysToArray(chordSequence);
    })

    /**
     * Add and remove notes from notes set
     * @param e
     */
    function handleMidi(e) {
        
        console.log(chordSequence)
        let { midi_event, note, velocity } = e.detail.midi;
        if (midi_event === MIDI_MESSAGE.on) {
            notes.add(note);
        } else {
            notes.delete(note);
        }

        chordSequence = chordSequence.slice(1)

    }

</script>


<h1>Broken Chords</h1>

<MidiListener on:midi={handleMidi} />

<ChordSequence chordSequence={chordSequence}></ChordSequence>


