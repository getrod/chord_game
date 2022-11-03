<script context="module" >
    /**
     * 
     * @param {Set<number>} n1
     * @param {Set<number>} n2
     */
    export function notesMatch(n1 , n2) {
        if (n1.size !== n2.size) return false;
        let result = true;
        n1.forEach((note) => {
            if (!n2.has(note)) result = false;
        })
        return result;
    }
</script>