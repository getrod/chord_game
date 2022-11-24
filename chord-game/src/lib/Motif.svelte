<script context="module">
	import { asyncEmit } from './Socket.svelte';

	export async function compileMotif(motifStr) {
		return await asyncEmit(
			'motif_compile',                // request
			'motif_compile_complete',       // result
			'motif_compile_error',          // error
			motifStr
		);
	}
</script>
