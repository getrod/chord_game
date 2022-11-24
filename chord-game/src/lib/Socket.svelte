<script context="module">
    import io from 'socket.io-client';

    export const socket = io('http://localhost:3000');

    // https://medium.com/@nikolozz/using-socket-io-with-async-await-13fa8c2dc9d9
	export function asyncEmit(reqEventName, resEventName, errEventName, data) {
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
</script>