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

    /**
     * Adds all the elements in set s
     * by the number num
     * 
     * Ex: setAdd({4,5,6}, 1) = {5,6,7}
     * @param {Set<number>} s
     * @param {number} num
     * @returns {Set<number>}
     */
    export function setAdd(s, num) {
        let newS = new Set();
        s.forEach((oldNum) => {
            newS.add(oldNum + num)
        })
        return newS;
    }

    /**
     * Modulo's all numbers in set s
     * by the number num
     * 
     * @param {Set<number>} s
     * @param {number} num
     * @returns {Set<number>}
     */
    export function setModulo(s, num) {
        let newS = new Set();
        s.forEach((oldNum) => {
            newS.add(oldNum % num)
        })
        return newS;
    }
    
    /**
     * A modulo without negative numbers.
     * 
     * Ex: -1 % 5 = -1
     * Ex: mod(-1, 5) = 4 
     * @param {number} n1
     * @param {number} n2
     */
    export function mod(n1, n2) {
        return ((n1 % n2) + n2) % n2;
    }
    
</script>