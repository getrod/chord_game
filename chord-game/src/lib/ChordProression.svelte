<!-- Maybe name this ChordSequnece -->
<script context="module">
    import { chordFormulas, noteNames } from './Chord.svelte'
    
    /**
     * Takes a string of the format "<interval>-<chord_name>"" ...
     * and converts them into general chord rules
     * 
     * ex: "0-maj 5-maj 7-maj" is the I, IV, V 
     *      chord progression
     * 
     * For diatonic chord naming, wrap the numbers in brackets
     * 
     * ex: "[1]-maj [3]-m [4]-maj [2]-m" is the 
     *      I, iii, IV, ii chord progression
     */
    export function parseChordProgressionText(chordProgStr) {
        // split string by space
        const chordTokens = chordProgStr.split(" "); 
        // for each general_chord
        let abstractChords = []
        let valid = true
        chordTokens.forEach((chordToken) => {
            // split by '-'
            const splitToken = chordToken.split('-')
            if (splitToken.length != 2) {
                console.log(`input not in the right format`)
                valid = false
                return
            }
            const intervalStr = splitToken[0]
            const chordName = splitToken[1]
            let interval = -1
            
            // if the interval section has brackets
            if (intervalStr.endsWith('[', 1) && intervalStr.endsWith(']')) {
                
                // convert diatonic chord number to 
                // chromatic scale number
                let diatonicNumber = parseInt(intervalStr.slice(1, -1))
                if ( diatonicNumber < 1 || diatonicNumber > 7 ) { 
                    console.log(`diatonic number ${diatonicNumber} not in range [1-7]`)
                    valid = false
                    return
                }
                let diatonicScaleIntervals = [0, 2, 4, 5, 7, 9, 11]
                interval = diatonicScaleIntervals[diatonicNumber - 1]
            } else {
                // check that the interval number is in [0-11] range
                interval = parseInt(intervalStr)
            }

            if ( interval < 0 || interval > 11) { 
                console.log(`interval ${interval} not in range [0-11]`)
                valid = false
                return
            }
            // check that chord name exists
            let exist = chordFormulas.reduce((prev, curr) => prev || curr.name === chordName, false)
            if (!exist) {
                console.log(`chord: ${chordName} is not defined`)
                valid = false
                return 
            }

            // append chord in a list
            abstractChords.push({interval: interval, name: chordName})
        })
        
        if (!valid) {
            return []
        } 
        return abstractChords
    }

    /**
     * Turns an abstract chord progression into a
     * chord progression of the specified key
     * @param chordProgStr
     * @param key
     */
    export function getChordProgression(chordProgStr, key) {
        let abstractChords = parseChordProgressionText(chordProgStr)
        let chords = []
        abstractChords.forEach((abstChord) => {
            let keyName = noteNames[(key + abstChord.interval) % 12]
            chords.push(keyName + abstChord.name)
        })
        return chords
    }

    export function addKeysToChordSequence(chordSequence) {
        chordSequence.forEach((chord, index) => chordSequence[index] = {id: index, name: chord})
        return chordSequence
    }
</script>