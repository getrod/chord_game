<script>
	import { onDestroy, onMount } from 'svelte';
	import { BrokenChord, BrokenChordSeq, Chord } from '../lib/ChordSequence.svelte';
	import { Midi, TrackEvent, MIDI_MESSAGE } from '../lib/Util.svelte';
	import io from 'socket.io-client';
	import { chordToChromatic, gridToChromatic } from '../lib/Validate.svelte';
	import { noteNames, noteNumber } from '../lib/Chord.svelte';

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
		ChordTrackEvent(0, 3 / 4, BrokenChord('E', 'm7', [3, 5]), 4),
		ChordTrackEvent(0, 1 / 4, BrokenChord('E', 'm7', [6]), 4),
		ChordTrackEvent(0, 1 / 4, BrokenChord('E', 'm7', [7, 9]), 4),
		ChordTrackEvent(0, 1 / 4, BrokenChord('E', 'm7', [8]), 4),
		ChordTrackEvent(0, 1 / 4, BrokenChord('E', 'm7', [6]), 4)
	];

	let track = [
		...ChordTrackEvent(0, 1 + 1 / 2, BrokenChord('A', 'm9', [3, 4, 5, 6, 7]), 3).events,
		...ChordTrackEvent(1 + 1 / 2, 1 + 1 / 2, BrokenChord('B', 'm7', [3, 4, 5, 6]), 3).events,
		...ChordTrackEvent(3, 2, BrokenChord('C', 'maj9', [0, 1, 2, 3, 4]), 5).events
	];

	/**
	 *
	 * @param startBeat
	 * @param duration
	 * @param {BrokenChord} brokenChord
	 * @param {number} octave transpose the broken chord to an octave
	 */
	function ChordTrackEvent(startBeat, duration, brokenChord, octave = undefined) {
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
	function BrokenChordSeqTrackEvent(brokenChordSeq, durations, octave = undefined) {
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
