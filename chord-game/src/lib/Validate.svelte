<script context="module" >
    import { isSetEqual } from './Math.svelte'
    /**
     * 
     * @param {Set<number>} n1
     * @param {Set<number>} n2
     */
    export function notesMatch(n1 , n2) {
        return isSetEqual(n1, n2);
    }
</script>