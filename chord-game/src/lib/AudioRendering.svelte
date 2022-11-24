<script context="module">
	import { asyncEmit } from './Socket.svelte';

	export async function renderTrackAudio(track, bpm) {
		return await asyncEmit('track_audio_req', 'track_audio_res', undefined, {
			track: track,
			bpm: bpm
		});
	}
</script>
