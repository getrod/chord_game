<script context="module">
    /**
     * Compares two sets for equality
     * @param {Set<number>} s1 first set
     * @param {Set<number>} s2 second set
     */
    export function isSetEqual(s1, s2) {
        if (s1.size !== s2.size) return false;
        let result = true;
        s1.forEach((note) => {
            if (!s2.has(note)) result = false;
        })
        return result;
    }

    
</script>