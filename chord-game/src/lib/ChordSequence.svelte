<script context="module">
    import { chordFormulas, noteNames } from './Chord.svelte';
    export function chordGeneratorRandom(length) {
        // random combination of keys and chords
        let randomChords = []
        for (let i = 0; i < length; i++) {
            let randomNote = noteNames[Math.floor(Math.random() * noteNames.length)]
            let randomChord = chordFormulas[Math.floor(Math.random() * chordFormulas.length)].name
            randomChords[i] = randomNote + randomChord
        }

        return randomChords
    }
</script>