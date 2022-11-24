<script>
	import { onMount } from 'svelte';
	import { BrokenChord, BrokenChordSeq } from '../lib/ChordSequence.svelte';
	import {
		Midi,
		TrackEvent,
		ChordTrackEvent,
		BrokenChordSeqTrackEvent,
		MIDI_MESSAGE, CHORD_TYPE
	} from '../lib/Util.svelte';
	import io from 'socket.io-client';
	import { chordToChromatic } from '../lib/Validate.svelte';
	import AudioComponent, {audioCtx} from '../component/AudioComponent.svelte';

	let _audio_event = undefined;
	let relativeTimeTrack = []
	let track = []

	let playAudio = false
	let renderAudio = false

	const socket = io('http://localhost:3000');
	socket.on('audio_event', (audio_event) => {
		_audio_event = audio_event;
	});

	socket.on('motif_compile_complete', (motif) => {
		console.log('yo')
		relativeTimeTrack = []
		console.log(motif)
		motif.forEach((chord) => {
			if(chord.type == CHORD_TYPE.chord) {
				relativeTimeTrack.push(
					ChordTrackEvent(
						0, 
						chord.duration,
						BrokenChord(chord.key, chord.chord_type, chord.notes),  
						chord.octave
					)
				)
			} else {
				relativeTimeTrack.push(
					BrokenChordSeqTrackEvent(
						BrokenChordSeq(chord.key, chord.chord_type, chord.note_seq),
						chord.duration_seq,
						chord.octave
					)
				)
			}
		})

		if (useRelativeTime) {
			// use relative time on tracks
			track = [];
			let currentBeat = 0;
			relativeTimeTrack.forEach((chordEvent) => {
				if (chordEvent.type == CHORD_TYPE.chord) {
					track.push(
						...ChordTrackEvent(
							currentBeat,
							chordEvent.duration,
							chordEvent.brokenChord,
							chordEvent.octave
						).events
					);
					currentBeat += chordEvent.duration;
				} else {
					chordEvent.chordEvents.forEach((chordTrackEvent) => {
						track.push(...ChordTrackEvent(
							currentBeat,
							chordTrackEvent.duration,
							chordTrackEvent.brokenChord,
							chordTrackEvent.octave
						).events)
						currentBeat += chordTrackEvent.duration;
					})
				}
			});
		}
		
	});

	socket.on('motif_compile_error', (e) => {
		console.log(e)
	});

	let bpm = 100;
	let useRelativeTime = true;
	let motifString = `Am9[3 4 5 6 7 | 3]-(3/2), Bm7[3 4 5 6 | 3]-(3/2), Cmaj9[0 1 2 3 4 | 5]-(2), 
	Em7<[3 5]-(3/4), [6]-(1/4), [7 9]-(1/4), [8]-(1/4), [6]-(1/4) | 4>,
	Em7<[3]-(1/4), [2]-(1/4), [3]-(1/4), [4]-(1/4), [1]-(1/4) | 4>,
	Em7[1 2 3 4 | 4]-(3/2),
	Cmaj9[0 1 2 3 4 | 5]-(5/2),
	Bm7[3 4 5 6 | 3]-(3/2),
	Am9[3 4 5 6 7 | 3]-(3/2)`


	function playBuffer() {
		if (!playAudio) {
			console.log('cant play audio')
			return
		}
		/**
		 * @type {AudioContext}
		 */
		//let audioCtx = new (window.AudioContext || window.webkitAudioContext)();
		if (!_audio_event) {console.log('no audio_event'); return;}
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

	async function compile_motif() {
		renderAudio = false
		playAudio = false
		await socket.emit('motif_compile', motifString);
		renderAudio = true
	}

	async function render_audio() {
		if (!renderAudio) {
			console.log('cant render audio')
			return
		}
		console.log('waiting for audio')
		await socket.emit('midi_track', { track: track, bpm: bpm });
		playAudio = true
		console.log('audio recieved')
	}

	onMount(() => {
		
		// socket.emit('midi_track', { track: track, bpm: bpm });
		console.log('test1')
		
		console.log('test2')
		// socket.emit('midi_track', { track: track, bpm: bpm });
		console.log('test3')
	});
</script>

<h1>Motif</h1>
<button on:click={compile_motif}>Compile Motif</button>
<button on:click={render_audio}>Render Audio</button>
<button on:click={playBuffer}>Play Sound</button>
<AudioComponent></AudioComponent>