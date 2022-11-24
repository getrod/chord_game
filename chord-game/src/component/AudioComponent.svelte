<script context="module">
    /**
     * @type {AudioContext}
     */
    export let audioCtx = undefined
    
    export function createBufferSource(audioEvent) {
        if (!audioCtx) return undefined
        let { audio_buffer, sample_rate, num_channels } = audioEvent;

		// audio buffer
		const buffer = audioCtx.createBuffer(
			num_channels,
			audio_buffer.length / num_channels,
			sample_rate
		);

        // fill audio buffer
		for (let channel = 0; channel < buffer.numberOfChannels; channel++) {
			const nowBuffering = buffer.getChannelData(channel);
			for (let i = 0; i < buffer.length; i++) {
				nowBuffering[i] = audio_buffer[i * 2 + channel];
			}
		}

        // connect to audioCtx
		const source = audioCtx.createBufferSource();
		source.buffer = buffer;
		source.connect(audioCtx.destination);
        return source
    }
</script>

<script>
	import { onMount } from 'svelte';

	onMount(() => {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    });
</script>
