<script>
	import MidiListener from '../component/MidiListener.svelte';
	import { chordInterpreter, notesToString } from '../lib/Chord.svelte';


	$: midi = []
	let notes = new Set()
	$: noteString = ''
	$: chord = []
	let midiNotesDisplay = []

	function handleMidi(event) {
		let { midi_event, note, velocity } = event.detail.midi
		midi = event.detail.midi;
		
		if (midi_event == 'note_on') notes.add(note)
		else notes.delete(note)

		noteString = notesToString(notes)

		console.log(noteString)

		chord = chordInterpreter(notes)
		midiNotesDisplay = Array.from(notes)
	}

</script>

<h1>Chord Game</h1>
<MidiListener on:midi={handleMidi}/>
<p>{midi.midi_event} {midi.note} {midi.velocity}</p>
<p>{noteString}</p>
<p>{midiNotesDisplay}</p>
<p>{chord}</p>
