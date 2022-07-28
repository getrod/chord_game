<script context="module">
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
    ]

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
</script>