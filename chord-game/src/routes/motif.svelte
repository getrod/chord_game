<script>
	import { onMount } from 'svelte';
	import { BrokenChord, BrokenChordSeq } from '../lib/ChordSequence.svelte';
	import {
		Midi,
		TrackEvent,
		ChordTrackEvent,
		BrokenChordSeqTrackEvent,
		MIDI_MESSAGE
	} from '../lib/Util.svelte';
	import io from 'socket.io-client';
	import { chordToChromatic } from '../lib/Validate.svelte';

	let _audio_event = undefined;

	const socket = io('http://localhost:3000');
	socket.on('audio_event', (audio_event) => {
		_audio_event = audio_event;
	});

	let bpm = 100;
	let useRelativeTime = true;

	let relativeTimeTrack = [
		ChordTrackEvent(0, 1 + 1 / 2, BrokenChord('A', 'm9', [3, 4, 5, 6, 7]), 3),
		ChordTrackEvent(0, 1 + 1 / 2, BrokenChord('B', 'm7', [3, 4, 5, 6]), 3),
		ChordTrackEvent(0, 2, BrokenChord('C', 'maj9', [0, 1, 2, 3, 4]), 5),

		...BrokenChordSeqTrackEvent(
			BrokenChordSeq('E', 'm7', [[3, 5], [6], [7, 9], [8], [6]]),
			[3 / 4, 1 / 4, 1 / 4, 1 / 4, 1 / 4],
			4
		),

		...BrokenChordSeqTrackEvent(
			BrokenChordSeq('E', 'm7', [[3], [2], [3], [4], [1]]),
			[1 / 4, 1 / 4, 1 / 4, 1 / 4, 1 / 4],
			4
		),

		ChordTrackEvent(0, 1 + 1 / 2, BrokenChord('E', 'm7', [1, 2, 3, 4]), 4),
		ChordTrackEvent(0, 2 + 1 / 2, BrokenChord('C', 'maj9', [0, 1, 2, 3, 4]), 5),
		ChordTrackEvent(0, 1 + 1 / 2, BrokenChord('B', 'm7', [3, 4, 5, 6]), 3),
		ChordTrackEvent(0, 1 + 1 / 2, BrokenChord('A', 'm9', [3, 4, 5, 6, 7]), 3)
	];

	let track = [
		...ChordTrackEvent(0, 1 + 1 / 2, BrokenChord('A', 'm9', [3, 4, 5, 6, 7]), 3).events,
		...ChordTrackEvent(1 + 1 / 2, 1 + 1 / 2, BrokenChord('B', 'm7', [3, 4, 5, 6]), 3).events,
		...ChordTrackEvent(3, 2, BrokenChord('C', 'maj9', [0, 1, 2, 3, 4]), 5).events
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
				nowBuffering[i] = audio_buffer[i * 2 + channel];
			}
		}

		// connect to audioCtx
		const source = audioCtx.createBufferSource();
		source.buffer = myArrayBuffer;
		source.connect(audioCtx.destination);
		source.start();
	}

	onMount(() => {
		if (useRelativeTime) {
			// use relative time on tracks
			track = [];
			let currentBeat = 0;
			relativeTimeTrack.forEach((chordEvent) => {
				track.push(
					...ChordTrackEvent(
						currentBeat,
						chordEvent.duration,
						chordEvent.brokenChord,
						chordEvent.octave
					).events
				);

				currentBeat += chordEvent.duration;
			});
		}
		socket.emit('midi_track', { track: track, bpm: bpm });
	});
</script>

<h1>Motif</h1>

<button on:click={playBuffer}>Play Sound</button>
