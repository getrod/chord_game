<script>
	import { onMount } from 'svelte';
	import { setIsEqual } from '../lib/Math.svelte';

    function test(condition, message) {
        console.log(`${condition ? 'PASS' : 'FAIL'}: ${message}`)
    }

	function set_is_equal_test() {
		test(setIsEqual(new Set([67, 72]), new Set([67, 72])) === true, "set equality");
		test(setIsEqual(new Set([67, 72]), new Set([67])) === false, "set inequality");
	}

    onMount(() => {
        set_is_equal_test()
    })
</script>
