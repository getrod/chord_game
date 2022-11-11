<script context="module" >
    import { isSetEqual, setAdd, setModulo } from './MathUtil.svelte'
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
     * @param {string} keyName 
     * @param {string} chordName
     */
    export function chordMatch(midi, keyName, chordName) {
        let match = false

        let chordKeyNum = noteNames.findIndex((name) => name === keyName)
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
    
    /**
     * Converts notes on a grid to notes on
     * the chromatic scale.
     * 
     * Ex: Given a C#maj grid (csGrid = {1, 5, 8}), and grid notes 
     * (csNotes = {15, 16, 17}) denoting the 15th, 16th, and 17th 
     * notes in the grid, the chromatic notes can be found by:
     * 
     * gridToChromatic(csGrid, csNotes) -> {61, 65, 68}
     *                 
     * @param {Set<number>} grid
     * @param {Set<number>} gridNotes
     * @returns {Set<number>} chromaticNotes
     */
    export function gridToChromatic(grid, gridNotes) {
        let chromaticNotes = new Set();
        let _grid = Array.from(grid).sort((a, b) => a-b)

        gridNotes.forEach((gridNote) => {
            // find the corresponding chromatic note to this grid
            let note = _grid[(gridNote % _grid.length)] + 12 * Math.floor(gridNote / _grid.length)
            chromaticNotes.add(note)
        })

        return chromaticNotes
    }

    /**
     * 
     * @param {string} keyName
     * @param {string} chordName
     * @param {Set<number>} gridNotes
     */
    export function chordToChromatic(keyName, chordName, gridNotes) {
        let keyNum = noteNames.findIndex((name) => name === keyName)
        let grid = new Set(chordFormula.get(chordName))

        if (!(keyNum !== -1 && grid)) return undefined

        grid = setAdd(grid, keyNum)
        return gridToChromatic(grid, gridNotes)
    }

    /**
     * Check if midi notes match the broken notes.
     * 
     * Ex: If midi = {14, 19}, gridNotes = {3, 5},
     * brokenChordMatch(midi, 'E', 'm7', gridNotes)) === true
     * 
     * If useOctave is true, chord match is dependent on the 
     * octave
     * @param {Set<number>} midi
     * @param {Set<number>} gridNotes
     * @param {string} keyName
     * @param {string} chordName
     * @param {boolean} useOctave 
     */
    export function brokenChordMatch(midi, keyName, chordName, gridNotes, useOctave = true) {
        let keyNum = noteNames.findIndex((name) => name === keyName)
        let grid = new Set(chordFormula.get(chordName))

        if (!(keyNum !== -1 && grid)) return false

        grid = setAdd(grid, keyNum)
        let notes = gridToChromatic(grid, gridNotes)
        let _midi = new Set(midi)

        if(!useOctave) {
            _midi = setModulo(_midi, 12)
            notes = setModulo(notes, 12)
        }
        
        return notesMatch(_midi, notes)
    }
</script>