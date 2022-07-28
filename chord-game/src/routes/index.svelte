<script>
	import io from 'socket.io-client';

	const socket = io('http://localhost:3000');

	$: midi = []

	socket.on('midi_event', (midi_event) => {
		midi = midi_event;
	});

	function sendMessage() {
		socket.emit('chat message', message);
		message = '';
	}
</script>

<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation tehehe</p>
<p>{midi}</p>
