<script>
	import { createEventDispatcher } from 'svelte';
	import io from 'socket.io-client';

	const socket = io('http://localhost:3000');
	const dispatch = createEventDispatcher();

	socket.on('midi_event', (midi_event) => {
		dispatch('midi', {
			midi: midi_event
		});
	});
</script>