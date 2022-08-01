<!-- Change name of file to RandomGenerator -->
<!-- Or remove this and put it in chord progression -->
<script context="module">
    import { chordFormulas, noteNames } from './Chord.svelte';
    export function chordGeneratorRandom(length, noteFilter=null, chordFilter=null) {
        // random combination of keys and chords
        let _noteNames = noteNames
        let _chordFormulas = chordFormulas

        if (noteFilter) {
            _noteNames = noteNames.filter(note => noteFilter.includes(note))
        }

        if (chordFilter) {
            _chordFormulas = chordFormulas.filter(chord => chordFilter.includes(chord.name))
        }

        let randomChords = []
        for (let i = 0; i < length; i++) {
            let randomNote = _noteNames[Math.floor(Math.random() * _noteNames.length)]
            let randomChord = _chordFormulas[Math.floor(Math.random() * _chordFormulas.length)].name
            randomChords[i] = randomNote + randomChord
        }
        return randomChords
    }
</script>