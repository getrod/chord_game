<script>
	import { onMount } from 'svelte';
	import { isSetEqual, setAdd } from '../lib/MathUtil.svelte';
    import { chordMatch, gridToChromatic } from '../lib/Validate.svelte';

    function test(condition, message) {
        console.log(`${condition ? 'PASS' : 'FAIL'}: ${message}`)
    }

    ////////////    TESTS    ////////////////

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

    function grid_to_chromatic_test() {
        let grids = new Map();
        grids.set('Am', new Set([9, 12, 16]))
        grids.set('Em7', new Set([14, 11, 7, 4]))


        test(
            isSetEqual(gridToChromatic(grids.get('Am'), new Set([0])), new Set([9])),
            'Am<[0]> === {9}' 
        )

        test(
            isSetEqual(gridToChromatic(grids.get('Am'), new Set([3])), new Set([21])),
            'Am<[3]> === {21}' 
        )

        test(
            isSetEqual(gridToChromatic(grids.get('Em7'), new Set([3, 5])), new Set([14, 19])),
            'Em7<[3, 5]> === {14, 19}' 
        )
    }

    function set_add_test() {
        test(
            isSetEqual(setAdd(new Set([4,5,6]), 1), new Set([5,6,7])),
            '{4,5,6} + 1 === {5,6,7}'
        )

        test(
            !isSetEqual(setAdd(new Set([4,5,6]), 1), new Set([6,7,8])),
            '{4,5,6} + 1 !== {6,7,8}'
        )
    }

    onMount(() => {
        set_is_equal_test()
        chord_match_test()
        grid_to_chromatic_test()
        set_add_test()
    })
</script>
