<script context="module">
	/**
	 * @typedef {object} Chord
	 * @param keyName
	 * @param chordName
	 */
	export function Chord(keyName, chordName) {
		return { 
			type: 'Chord',
			keyName: keyName, 
			chordName: chordName 
		};
	}


	/**
	 * ```
	 * Ex: BrokenChordSeq('E', 'm7', [[3, 5], [6], [7,9], [8]]) = [
	 *      BrokenChord('E', 'm7', [3, 5]),
	 *      BrokenChord('E', 'm7', [6]),
	 *      BrokenChord('E', 'm7', [7,9]),
	 *      BrokenChord('E', 'm7', [8]),
	 * ]
	 * ```
	 * @param keyName
	 * @param chordName
	 * @param {number[][]} gridNoteSeq
	 */
	export function BrokenChord(keyName, chordName, gridNoteSeq) {
		return {
			type: 'BrokenChord',
			keyName: keyName,
			chordName: chordName,
			sequence: gridNoteSeq
		};
	}
</script>
