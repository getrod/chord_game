<script context="module">
	import { chordToChromatic } from './Validate.svelte';
	import { BrokenChord, BrokenChordSeq } from '../lib/ChordSequence.svelte';

	export function addKeysToArray(array) {
		array.forEach((data, index) => (array[index] = { id: index, data: data }));
		return array;
	}

	export const MIDI_MESSAGE = {
		on: 'note_on',
		off: 'note_off'
	};

	export function Midi(midi_event, note, velocity) {
		return {
			midi_event: midi_event,
			note: note,
			velocity: velocity
		};
	}

	export function TrackEvent(beat, midi_event) {
        return {
            beat: beat,
            midi_event: midi_event
        }
    }

	/**
	 *
	 * @param startBeat
	 * @param duration
	 * @param {BrokenChord} brokenChord
	 * @param {number} octave transpose the broken chord to an octave
	 */
	 export function ChordTrackEvent(startBeat, duration, brokenChord, octave = undefined) {
		let notes = [];
		notes.push(
			...chordToChromatic(brokenChord.keyName, brokenChord.chordName, brokenChord.gridNotes)
		);

		let events = [];
		notes.forEach((note) => {
			if (octave) note = note + 12 * octave;
			events.push(TrackEvent(startBeat, Midi(MIDI_MESSAGE.on, note, 99)));
			events.push(TrackEvent(startBeat + duration, Midi(MIDI_MESSAGE.off, note, 0)));
		});
		return {
			startBeat: startBeat,
			duration: duration,
			events: events,
			brokenChord: brokenChord,
			octave: octave
		};
	}

	/**
	 * Can only use for relative timing
	 * @param {BrokenChordSeq} brokenChordSeq
	 * @param {number[]} durations
	 * @param octave
	 */
	export function BrokenChordSeqTrackEvent(brokenChordSeq, durations, octave = undefined) {
		let chordEvents = [];
		if (brokenChordSeq.sequence.length !== durations.length) return [];
		brokenChordSeq.sequence.forEach((notes, i) => {
			chordEvents.push(ChordTrackEvent(
				0, 
				durations[i], 
				BrokenChord('E', 'm7', notes), 
				octave
			));
		});

		return chordEvents;
	}
</script>
