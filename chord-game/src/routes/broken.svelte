<script>
	import { onMount } from 'svelte';
	import ChordList from '../component/ChordList.svelte';
	import ChordSequence from '../component/ChordSequence.svelte';
	import MidiListener from '../component/MidiListener.svelte';
	import { BrokenChordSeq, Chord } from '../lib/ChordSequence.svelte';
	import { addKeysToArray, MIDI_MESSAGE } from '../lib/Util.svelte';
	import { brokenChordMatch, chordMatch, notesMatch } from '../lib/Validate.svelte';

	let midi = new Set();
	let sequence = addKeysToArray([[62, 67], [71], [74, 79], [76]]);
	let _sequence = [
		Chord('C', 'maj'),
		Chord('D', 'm'),
		Chord('F', 'maj'),
		BrokenChordSeq('E', 'm7', [[3 + (4*2), 5 + (4*2)], [6 + (4*2)], [7+ (4*2), 9+ (4*2)], [8+ (4*2)]])
	];
	let displaySequence = [];

	onMount(() => {
		//console.log(sequence)
	});

	/**
	 * Add and remove notes from notes set &
	 * checks in notes match the sequence
	 * @param e
	 */
	function handleMidi(e) {
		let { midi_event, note, velocity } = e.detail.midi;
		if (midi_event === MIDI_MESSAGE.on) {
			midi.add(note);
		} else {
			midi.delete(note);
		}

		match();
		displaySequence = Array.from(_sequence);
		displaySequence = addKeysToArray(displaySequence);
		console.log(_sequence);
	}

	function verify(midi, chord) {
		if (chord.type === 'BrokenChord') {
			return brokenChordMatch(midi, chord.keyName, chord.chordName, chord.sequence[0]);
		} else {
			return chordMatch(midi, chord.keyName, chord.chordName);
		}
	}

	function match() {
		if (verify(midi, _sequence[0])) {
			if (_sequence[0].type === 'BrokenChord') {
                _sequence[0].sequence = _sequence[0].sequence.slice(1);
			} else {
				// remove the beginning element
				_sequence = _sequence.slice(1);
			}
		}
	}
</script>

<h1>Broken Chord</h1>

<MidiListener on:midi={handleMidi} />

<!-- <ChordSequence chordSequence={sequence}></ChordSequence> -->
<!-- <ChordList chords={displaySequence}></ChordList> -->
