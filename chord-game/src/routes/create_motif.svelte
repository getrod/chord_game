<script>
	import io from 'socket.io-client';
	const socket = io('http://localhost:3000');
	let motifStr = '';
    let error_message = ''
    let motif = []

	// https://medium.com/@nikolozz/using-socket-io-with-async-await-13fa8c2dc9d9
	function asyncEmit(reqEventName, resEventName, errEventName, data) {
		return new Promise(function (resolve, reject) {
			socket.emit(reqEventName, data);
			socket.on(resEventName, (result) => {
				socket.off(resEventName);
				resolve(result);
			});
			socket.on(errEventName, (e) => {
				reject(e);
			});
			setTimeout(reject, 10000);
		});
	}

	/**
	 * resceives string and returns the motif
	 */
	async function compileMotif() {
        error_message = ''
		try {
			const res = await asyncEmit(
				'motif_compile',
				'motif_compile_complete',
				'motif_compile_error',
				motifStr
			);
            console.log(res)
            motif = res
		} catch (error) {
            error_message = error
            console.log(error)
        }

		
	}
</script>

<label for="motif">Name (4 to 8 characters):</label>
<input bind:value={motifStr} id="motif" name="motif" />
<button on:click={compileMotif}>Compile</button>
<p>{error_message}</p>