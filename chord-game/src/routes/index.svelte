<script>
	import MidiListener from '../lib/MidiListener.svelte';
	import { chordFormulas, noteNames, chordInterpreter, notesToString } from '../lib/Chord.svelte';

	$: midi = []
	$: notes = new Set()
	$: chord = []

	function handleMidi(event) {
		let { midi_event, note, velocity } = event.detail.midi
		midi = event.detail.midi;
		
		if (midi_event == 'note_on') notes.add(note)
		else notes.delete(note)

		console.log(notesToString(notes))

		chord = chordInterpreter(notes)
	}

</script>

<h1>Chord Game</h1>
<MidiListener on:midi={handleMidi}/>
<p>{midi.midi_event} {midi.note} {midi.velocity}</p>
<p>{chord}</p>
