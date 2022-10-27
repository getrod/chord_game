<script context="module">
    export function addKeysToArray(array) {
        array.forEach((data, index) => array[index] = {id: index, data: data})
        return array
    }

    export const MIDI_MESSAGE = {
        on: 'note_on'
    }
</script>