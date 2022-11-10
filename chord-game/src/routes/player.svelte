<script>
	import { onDestroy, onMount } from "svelte";
	import { Midi, MIDI_MESSAGE } from "../lib/Util.svelte";
    import io from 'socket.io-client';
	import MidiListener from "../component/MidiListener.svelte";

	const socket = io('http://localhost:3000');

    let bpm = 120
    let ppq = 16 //parts per quarter note
    let millsecondsPerSecond = 1000
    let secondsPerMinute = 60
    let intervalTime = ((millsecondsPerSecond * secondsPerMinute) / (bpm)) / ppq
    let interval = undefined;
    let tick = 0

    let _prevTime = 0

    onMount(() => {
        interval = setInterval(intervalCallback, intervalTime);
        console.log(`interval: ${intervalTime}`)
    })

    onDestroy(() => {
        clearInterval(interval)
    })

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

    function TrackEvent(beat, midi_event) {
        return {
            tick: Math.floor(beat * ppq),
            midi_event: midi_event
        }
    }
    
    function intervalCallback() {
        track.forEach((trackEvent) => {
            if (trackEvent.tick === tick) {
                console.log(`tick ${tick}`)
                socket.emit('midi_track_event', trackEvent.midi_event)
            }
        })
        if (tick % ppq === 0) {console.log(`ms: ${Date.now() - _prevTime}`)}
        _prevTime = Date.now()
        tick++;
    }

    // onMount(() => {
    //     socket.emit('midi_track_event', Midi(MIDI_MESSAGE.on, 60, 99))
    //     socket.emit('midi_track_event', Midi(MIDI_MESSAGE.on, 64, 99))
    //     socket.emit('midi_track_event', Midi(MIDI_MESSAGE.on, 67, 99))
    // })

    function handleMidi(e) {
		let { midi_event, note, velocity } = e.detail.midi;
        console.log(e.detail.midi)
		socket.emit('midi_track_event', e.detail.midi)
	}
</script>

<h1>Player</h1>
<MidiListener on:midi={handleMidi}></MidiListener>

<button on:click={() => {clearInterval(interval)}}>Stop Interval</button>