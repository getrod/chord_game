<script context="module" >
    import { isSetEqual } from './Math.svelte'
    import { noteNames, chordFormula } from './Chord.svelte'
    /**
     * Checks if two sets of notes are equal.
     * @param {Set<number>} n1
     * @param {Set<number>} n2
     */
    export function notesMatch(n1 , n2) {
        return isSetEqual(n1, n2);
    }

    /**
     * Checks if the midi notes match a chord.
     * 
     * Ex: chordMatch(midi, 'C', 'maj')
     * @param {Set<number>} midi midi input
     * @param {string} chordKey 
     * @param {string} chordName
     */
    export function chordMatch(midi, chordKey, chordName) {
        let match = false

        let chordKeyNum = noteNames.findIndex((name) => name === chordKey)
        let chordIntervals = chordFormula.get(chordName)
        let chordSet = new Set();
        
        if (chordKeyNum !== -1 && chordIntervals) {
            // transpose chord intervals to the requested key
            for (let i = 0; i < chordIntervals.length; i++) {
                chordSet.add((chordIntervals[i] + chordKeyNum) % 12)
            }

            // convert midi into a modulo 12 set
            let midiModSet = new Set()
            midi.forEach((note) => {
                midiModSet.add(note % 12)
            })

            match = notesMatch(midiModSet, chordSet)
        } 

        return match
    }
</script>