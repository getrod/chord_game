<script context="module">
    /**
     * TODO: Depricate?
     */
    export const chordFormulas = [
        {
            name: 'maj',
            intervals: [0, 4, 7]
        },
        {
            name: 'm',
            intervals: [0, 3, 7]
        },
        {
            name: 'sus2',
            intervals: [0, 2, 7]
        },
        {
            name: 'sus4',
            intervals: [0, 5, 7]
        },
        {
            name: 'maj7',
            intervals: [0, 4, 7, 11]
        },
        {
            name: 'm7',
            intervals: [0, 3, 7, 10]
        },
        {
            name: 'maj9',
            intervals: [0, 2, 4, 7, 11]
        },
        {
            name: 'm9',
            intervals: [0, 2, 3, 7, 10]
        },
    ]

    /**
     * @type {Map<string, Array<number>>}
     */
    export const chordFormula = new Map();
    chordFormula.set('maj',  [0, 4, 7])
    chordFormula.set('m',  [0, 3, 7])
    chordFormula.set('sus2',  [0, 2, 7])
    chordFormula.set('sus4',  [0, 5, 7])
    chordFormula.set('maj7',  [0, 4, 7, 11])
    chordFormula.set('maj9',  [0, 2, 4, 7, 11])
    chordFormula.set('m9',  [0, 2, 3, 7, 10])

    export const noteNames = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'G#', 'A', 'Bb', 'B']

    export function noteName(noteNumber) {
		return noteNames[noteNumber % noteNames.length]
	}

	export function noteOctave(noteNumber) {
		return Math.trunc(noteNumber / noteNames.length)
	}

    export function notesToString(notes) {
		let s = '['
		if (notes.size > 0) {
			notes.forEach(note => s += ` ${noteName(note)}${noteOctave(note)},`)
		}
		s += ']'
		return s
	}


    export function chordInterpreter(noteNumbers) {
		let noteNumSet = new Set()
		noteNumbers.forEach((noteNum) => noteNumSet.add(noteNum % 12))
		
		let chords = []
		noteNumSet.forEach((key) => {
			let tempSet = Array.from(noteNumSet)	
			tempSet.forEach((noteNum, i) => {
				tempSet[i] = (noteNum - key) % 12
				if (tempSet[i] < 0) tempSet[i] += 12 
			})
			tempSet.sort()
			chordFormulas.forEach((chordFormula) => {
				let set1 = new Set(chordFormula.intervals)
				let set2 = new Set(tempSet)
				set1.forEach((interval) => set2.delete(interval))
				if (set2.size == 0 && tempSet.length == chordFormula.intervals.length) {
					chords.push(noteName(key) + chordFormula.name)
				}
			})
		})
		
		return chords
	}

    /**
     * Takes an array of note numbers and returns
     * @param notes: note numbers
     * @param chord: ex: 'F#maj' 
     */
    export function chordMatch(notes, chord) {
        let chordNames = chordInterpreter(notes)
        let match = false
        chordNames.forEach((chordName) => {
            if (chordName === chord) {
                match = true
            }
        })
        return match
    }
</script>