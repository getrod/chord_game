<script>
    import { createEventDispatcher } from 'svelte';
	import MidiListener from './MidiListener.svelte';

    const dispatch = createEventDispatcher();
	let notes = new Set();
    
	function handleMidi(event) {
		let { midi_event, note, velocity } = event.detail.midi;
		if (midi_event == 'note_on') {
			notes.add(note);
			dispatch('noteAdd', {
            	activeNotes: notes
        	});
		} else {
			notes.delete(note);
			dispatch('noteRemove', {
            	activeNotes: notes
        	});
		}

        dispatch('note', {
            activeNotes: notes
        });
	}
</script>

<MidiListener on:midi={handleMidi} />
