<script>
	import { onMount } from 'svelte';
	import { isSetEqual } from '../lib/Math.svelte';
    import { chordMatch } from '../lib/Validate.svelte';

    function test(condition, message) {
        console.log(`${condition ? 'PASS' : 'FAIL'}: ${message}`)
    }

    ////////////    TEST    ////////////////

	function set_is_equal_test() {
		test(isSetEqual(new Set([67, 72]), new Set([67, 72])) === true, "set equality");
		test(isSetEqual(new Set([67, 72]), new Set([67])) === false, "set inequality");
	}

    function chord_match_test() {
        test(chordMatch(new Set([12, 24, 28, 31]), 'C', 'maj') === true, 
            '[12, 24, 28, 31] is Cmaj'
            )
        
        test(chordMatch(new Set([12, 24, 28, 31]), 'F', 'maj') === false, 
            '[12, 24, 28, 31] is not Fmaj'
            )  
            
        test(chordMatch(new Set([53, 60, 69]), 'F', 'maj') === true, 
            '[53, 60, 69] is Fmaj'
            )  
        
        test(chordMatch(new Set([65, 64, 60, 62, 69]), 'D', 'm9') === true, 
            '[65, 64, 60, 62, 69] is Dm9'
            ) 
    }

    onMount(() => {
        set_is_equal_test()
        chord_match_test()
    })
</script>
