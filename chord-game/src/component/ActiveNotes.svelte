<script>
    import { createEventDispatcher } from 'svelte';
	import MidiListener from './MidiListener.svelte';

    const dispatch = createEventDispatcher();
	let notes = new Set();
    
	function handleMidi(event) {
		let { midi_event, note, velocity } = event.detail.midi;
		if (midi_event == 'note_on') {
			notes.add(note);
			dispatch('add_note', {
            	note: note
        	});
		} else {
			notes.delete(note);
			dispatch('remove_note', {
            	note: note
        	});
		}

        dispatch('note', {
            activeNotes: notes
        });
	}
</script>

<MidiListener on:midi={handleMidi} />
