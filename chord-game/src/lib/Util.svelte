<script context="module">
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
</script>
