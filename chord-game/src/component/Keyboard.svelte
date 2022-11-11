<script>
import { onMount } from "svelte";
import { addKeysToArray } from '../lib/Util.svelte'


	export let lowestNote = 36;
	export let highestNote = 96;
    export const intervalRange = 17
    export let rangeStartNoteR
    export let rangeStartNoteL 
    let notes = []

    onMount(() => {
        for(let i = lowestNote; i <= highestNote; i++ ) {
            notes.push(i)
        }
        notes = addKeysToArray(notes)
    })

    function inRange(note, startNote) {
        return note >= startNote && note < startNote + intervalRange
    }

    function highlightNote(note) {
        if (inRange(note, rangeStartNoteR) || inRange(note, rangeStartNoteL)) {
            return 'highlight'
        }
    }

</script>

<div class="keys">
    <!-- octave -->
    {#each notes as note (note.id)}
        {#if (note.id % 12) === 0} 
            <div class="white note {highlightNote(note.data)}" />
        {:else if (note.id % 12) === 1}
            <div class="black note g {highlightNote(note.data)}" />
        {:else if (note.id % 12) === 2}
            <div class="white note g {highlightNote(note.data)}" />
        {:else if (note.id % 12) === 3}
            <div class="black note g {highlightNote(note.data)}" />
        {:else if (note.id % 12) === 4}
            <div class="white note g {highlightNote(note.data)}" />
        {:else if (note.id % 12) === 5}    
            <div class="white note {highlightNote(note.data)}" />
        {:else if (note.id % 12) === 6}
            <div class="black note g {highlightNote(note.data)}" />
        {:else if (note.id % 12) === 7}
            <div class="white note g {highlightNote(note.data)}" /> 
        {:else if (note.id % 12) === 8}
            <div class="black note g {highlightNote(note.data)}" />
        {:else if (note.id % 12) === 9}
            <div class="white note g {highlightNote(note.data)}" />
        {:else if (note.id % 12) === 10}
            <div class="black note g {highlightNote(note.data)}" />
        {:else}
            <div class="white note g {highlightNote(note.data)}" /> 
        {/if}
    {/each}
    
</div>


<style>
    .keys {
        position:relative;
    }
    .keys div:last-child {
        border-right: .7px solid #bbb;
    }
    .note {
        position:relative;
        float: left;
        padding: 0;
        margin: 0;
    }
	.white {
		height: 8em;
		width: 2em;
        z-index: 1;
        position:relative;
		background-color: #fff;
		border-left: 1px solid #bbb;
		border-bottom: 1px solid #bbb;
        border-top: 1px solid #bbb;
	}
    .black {
        height: 4.5em;
		width: 1em;
        z-index: 2;
		background-color: #000;
		border-left: 1px solid #000;
		border-bottom: 1px solid #000;
    }
    .highlight {
        background-color: blue;
        border-left: 1px solid black;
		border-bottom: 1px solid black;
    }
    .g {
        margin:0 0 0 -0.5em
    }
</style>