<script>
	import { onMount } from "svelte";
    import ChordSequence from "../component/ChordSequence.svelte";
    import MidiListener from "../component/MidiListener.svelte";
	import { addKeysToArray, MIDI_MESSAGE } from "../lib/Util.svelte";
	import { notesMatch } from "../lib/Validate.svelte";

    let notes = new Set();
    let sequence = addKeysToArray([[62, 67], [71], [74, 79], [76]]);

    onMount(() => {
        console.log(sequence)
    })

    /**
     * Add and remove notes from notes set &
     * checks in notes match the sequence
     * @param e
     */
    function handleMidi(e) {
        
        let { midi_event, note, velocity } = e.detail.midi;
        if (midi_event === MIDI_MESSAGE.on) {
            notes.add(note);
        } else {
            notes.delete(note);
        }

        match()
    }

    function match() {
        if (notesMatch(new Set(sequence[0].data), notes)) {
            // remove the beginning element 
            sequence = sequence.slice(1);
        }
    }

</script>


<h1>Broken Chord</h1>

<MidiListener on:midi={handleMidi} />

<ChordSequence chordSequence={sequence}></ChordSequence>