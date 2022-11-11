<script>
	import ChordList from '../component/ChordList.svelte';
	import MidiListener from '../component/MidiListener.svelte';
	import { BrokenChordSeq, Chord } from '../lib/ChordSequence.svelte';
	import { MIDI_MESSAGE } from '../lib/Util.svelte';
	import { brokenChordMatch, chordMatch, notesMatch } from '../lib/Validate.svelte';

	let midi = new Set();
	let _sequence = [
		Chord('A', 'm9'),
		Chord('B', 'm7'),
		Chord('C', 'maj9'),
        BrokenChordSeq('E', 'm7', [[3 , 5], [6], [7, 9], [8], [6]]),
        BrokenChordSeq('E', 'm7', [[3], [2], [3], [4], [1]]),
	];

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
	}

	function verify(midi, chord) {
		if (chord.type === 'BrokenChord') {
			return brokenChordMatch(midi, chord.keyName, chord.chordName, chord.sequence[0], false);
		} else {
			return chordMatch(midi, chord.keyName, chord.chordName);
		}
	}

	function match() {
        // if no more chords, return
        if (_sequence.length === 0) return

		if (verify(midi, _sequence[0])) {
			if (_sequence[0].type === 'BrokenChord') {
                _sequence[0].sequence = _sequence[0].sequence.slice(1);
                if (_sequence[0].sequence.length === 0) {
                    // if nothing left in broken sequence, remove broken chord
                    _sequence = _sequence.slice(1);
                }
			} else {
				// remove the beginning chord
				_sequence = _sequence.slice(1);
			}
            midi.clear()
		}
	}
</script>

<h1>Broken Chord</h1>

<MidiListener on:midi={handleMidi} />

<ChordList chords={_sequence}></ChordList>
