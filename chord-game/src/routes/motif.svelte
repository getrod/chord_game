<script>
	import { onDestroy, onMount } from 'svelte';
	import { Midi, TrackEvent, MIDI_MESSAGE } from '../lib/Util.svelte';
	import io from 'socket.io-client';

	let _audio_event = undefined;

	const socket = io('http://localhost:3000');
	socket.on('audio_event', (audio_event) => {
		_audio_event = audio_event;
	});

	let bpm = 120;

	let track = [
		TrackEvent(0, Midi(MIDI_MESSAGE.on, 60, 99)),
		TrackEvent(0, Midi(MIDI_MESSAGE.on, 64, 99)),
		TrackEvent(0, Midi(MIDI_MESSAGE.on, 67, 99)),

		TrackEvent(1, Midi(MIDI_MESSAGE.off, 60, 99)),
		TrackEvent(1, Midi(MIDI_MESSAGE.off, 64, 99)),
		TrackEvent(1, Midi(MIDI_MESSAGE.off, 67, 99)),

		TrackEvent(1, Midi(MIDI_MESSAGE.on, 60 + 2, 99)),
		TrackEvent(1, Midi(MIDI_MESSAGE.on, 64 + 2, 99)),
		TrackEvent(1, Midi(MIDI_MESSAGE.on, 67 + 2, 99)),

		TrackEvent(2, Midi(MIDI_MESSAGE.off, 60 + 2, 99)),
		TrackEvent(2, Midi(MIDI_MESSAGE.off, 64 + 2, 99)),
		TrackEvent(2, Midi(MIDI_MESSAGE.off, 67 + 2, 99)),

		TrackEvent(2, Midi(MIDI_MESSAGE.on, 60 + 4, 99)),
		TrackEvent(2, Midi(MIDI_MESSAGE.on, 64 + 4, 99)),
		TrackEvent(2, Midi(MIDI_MESSAGE.on, 67 + 4, 99)),

		TrackEvent(3, Midi(MIDI_MESSAGE.off, 60 + 4, 99)),
		TrackEvent(3, Midi(MIDI_MESSAGE.off, 64 + 4, 99)),
		TrackEvent(3, Midi(MIDI_MESSAGE.off, 67 + 4, 99))
	];

	function playBuffer() {
		/**
		 * @type {AudioContext}
		 */
		let audioCtx = new (window.AudioContext || window.webkitAudioContext)();
		if (!_audio_event) return;
		let { audio_buffer, sample_rate, num_channels } = _audio_event;

		// audio buffer
		const myArrayBuffer = audioCtx.createBuffer(
			num_channels, 
			audio_buffer.length / num_channels, 
			sample_rate
		);

		// fill audio buffer
		for (let channel = 0; channel < myArrayBuffer.numberOfChannels; channel++) {
			const nowBuffering = myArrayBuffer.getChannelData(channel);
			for (let i = 0; i < myArrayBuffer.length; i++) {
				nowBuffering[i] = audio_buffer[(i * 2) + channel];
			}
		}

		// connect to audioCtx
		const source = audioCtx.createBufferSource();
		source.buffer = myArrayBuffer;
		source.connect(audioCtx.destination);
		source.start();
	}

	onMount(() => {
		socket.emit('midi_track', { track: track, bpm: bpm });
	});
</script>

<h1>Motif</h1>

<button on:click={playBuffer}>Play Sound</button>
