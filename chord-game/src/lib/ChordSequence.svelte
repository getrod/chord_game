<script context="module">
	/**
	 * @tyedef {{type: string; keyName: string; chordName: string;}} Chord
	 * @tyedef {{type: string; keyName: string; chordName: string; gridNotes: Set<number>;}} BrokenChord
	 * @typedef {{
			type: string;
			keyName: any;
			chordName: any;
			sequence: number[][];
		}} BrokenChordSeq
	*/

	/**
	 * @param {string} keyName
	 * @param {string} chordName
	 */
	export function Chord(keyName, chordName) {
		return { 
			type: 'Chord',
			keyName: keyName, 
			chordName: chordName 
		};
	}

	/**
	 * 
	 * @param {string} keyName
	 * @param {string} chordName
	 * @param {Set<number>} gridNotes
	 */
	export function BrokenChord(keyName, chordName, gridNotes) {
		return { 
			type: 'Chord',
			keyName: keyName, 
			chordName: chordName,
			gridNotes: gridNotes
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
	export function BrokenChordSeq(keyName, chordName, gridNoteSeq) {
		return {
			type: 'BrokenChord',
			keyName: keyName,
			chordName: chordName,
			sequence: gridNoteSeq
		};
	}
</script>
