<script>
	import { onDestroy, onMount } from "svelte";
	import { Midi, TrackEvent, MIDI_MESSAGE } from "../lib/Util.svelte";
    import io from 'socket.io-client';
	import MidiListener from "../component/MidiListener.svelte";

	const socket = io('http://localhost:3000');

    let bpm = 120

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
        TrackEvent(3, Midi(MIDI_MESSAGE.off, 67 + 4, 99)),
    ]
    
    onMount(() => {
        socket.emit('midi_track', {track: track, bpm: bpm})
    })

</script>

<h1>Player</h1>
<button on:click={() => {socket.emit('midi_track', {track: track, bpm: bpm})}}>Play</button>