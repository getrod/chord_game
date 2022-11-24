<script>
	import { onMount } from 'svelte';
	import { BrokenChord, BrokenChordSeq } from '../lib/ChordSequence.svelte';
	import {
		ChordTrackEvent,
		BrokenChordSeqTrackEvent,
		CHORD_TYPE
	} from '../lib/Util.svelte';
	import {socket, asyncEmit} from '../lib/Socket.svelte'
	import {compileMotif} from '../lib/Motif.svelte'
	import {renderTrackAudio} from '../lib/AudioRendering.svelte'
	import AudioComponent, {createBufferSource} from '../component/AudioComponent.svelte';

	let _audio_event = undefined;
	let track = []
	let playAudio = false
	let renderAudio = false
	let _source = undefined

	function motif2Track(motif) {
		console.log('yo')
		let relativeTimeTrack = []
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
		return track
	}

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


	function play_sound() {
		if (!playAudio) {
			console.log('cant play audio')
			return
		}
		
		if (!_audio_event) {console.log('no audio_event'); return;}

		_source = createBufferSource(_audio_event)
		_source.start()
	}

	async function compile_motif() {
		renderAudio = false
		playAudio = false
		let motif = undefined
		try {
			motif = await compileMotif(motifString);
			track = motif2Track(motif)
			renderAudio = true
		} catch (error) {
			console.log(error)
		}
	}

	async function render_audio() {
		if (!renderAudio) {
			console.log('cant render audio')
			return
		}
		console.log('waiting for audio')

		_audio_event = await renderTrackAudio(track, bpm)
		playAudio = true
		console.log('!!audio recieved!!')
	}

</script>

<h1>Motif</h1>
<button on:click={compile_motif}>Compile Motif</button>
<button on:click={render_audio}>Render Audio</button>
<button on:click={play_sound}>Play Sound</button>
<AudioComponent></AudioComponent>