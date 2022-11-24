<script>
    import {compileMotif} from '../lib/Motif.svelte'
	let motifStr = '';
    let error_message = ''
    let motif = []

	/**
	 * resceives string and returns the motif
	 */
	async function handleClick() {
        error_message = ''
		try {
			const res = await compileMotif(motifStr);
            console.log(res)
            motif = res
		} catch (error) {
            error_message = error
            console.log(error)
        }

		
	}
</script>

<label for="motif">Motif:</label>
<input bind:value={motifStr} id="motif" name="motif" />
<button on:click={handleClick}>Compile</button>
<p>{error_message}</p>