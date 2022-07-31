<script>
    import Keyboard from '../component/Keyboard.svelte'
    import { chordMatch } from '../lib/Chord.svelte'
    import { chordGeneratorRandom } from '../lib/ChordSequence.svelte'
    import ActiveNotes from '../lib/ActiveNotes.svelte'
    import { onMount } from 'svelte'
    import { addKeysToArray } from '../lib/Util.svelte'
    /**
     * specifiy range of keybaord
     * 
     * when a chord appears on the screen, play its inversions up and down the keybaord
     * There will be a blue region highlighting where to press the keys
     * 
     * For every random number of successes between 5-10, add a new chord
     * 
     * Game lasts 3 minutes
    */
    let lowestNote = 36;
	let highestNote = 96;
    const intervalRange = 17
    let rangeStartNoteR = 60
    let rangeStartNoteL = 36
    let chord = chordGeneratorRandom(1)[0]
    let score = 0
    const randomNumSuccess = () => Math.random() * 5 + 5
    let numSuccess = randomNumSuccess()
    let jumpSpeed = 5
    let directionL = jumpSpeed
    let directionR = jumpSpeed
    let keyboardNotes = []
    let activeNotes = []

    onMount(() => {
        for(let i = lowestNote; i <= highestNote; i++ ) {
            keyboardNotes.push(i)
        }
        keyboardNotes = addKeysToArray(keyboardNotes)
    })

    function noteInRange(note, startNote) {
        return note >= startNote && note < startNote + intervalRange
    }

    function highlightNote(note, R, L) {
        if (noteInRange(note, rangeStartNoteR) || noteInRange(note, rangeStartNoteL)) {
            return 'highlight'
        }
    }
    
    function handleOnNote(e) {
        activeNotes = e.detail.activeNotes
        let validRange = true
        activeNotes.forEach((note) => {
            validRange = validRange &&
                ( noteInRange(note, rangeStartNoteR) || noteInRange(note, rangeStartNoteL) )
        });

        if (!validRange) {
            return
        }

        if (chordMatch(activeNotes, chord)) {
            // add to some score
            score += 10

            // nudge the interval range
            if (rangeStartNoteL <= lowestNote) {
                directionL = jumpSpeed
            } else if (rangeStartNoteL + intervalRange >= rangeStartNoteR) {
                directionL = -1 * jumpSpeed
            }
            
            if (rangeStartNoteR <= lowestNote) {
                directionR = jumpSpeed
            } else if (rangeStartNoteR + intervalRange >= highestNote) {
                directionR = -1 * jumpSpeed
            }

            rangeStartNoteR += directionR
            rangeStartNoteL += directionL

            console.log(rangeStartNoteR)
            numSuccess--
            if (numSuccess === 0) {
                // get new chord
                chord = chordGeneratorRandom(1)[0]
            }
        }
    }

    function handleonclick() {
        rangeStartNoteR += directionR
            rangeStartNoteL += directionL
            console.log(rangeStartNoteR)
    }
</script>


<h1>{chord}</h1>
<h2>Score {score}</h2>
<ActiveNotes on:noteAdd={handleOnNote} />
<div class="keys">
    {#each keyboardNotes as note (note.id)}
        {#if (note.id % 12) === 0} 
            <div class="white note {highlightNote(note.data, rangeStartNoteR, rangeStartNoteL)}" />
        {:else if (note.id % 12) === 1}
            <div class="black note g {highlightNote(note.data, rangeStartNoteR, rangeStartNoteL)}" />
        {:else if (note.id % 12) === 2}
            <div class="white note g {highlightNote(note.data, rangeStartNoteR, rangeStartNoteL)}" />
        {:else if (note.id % 12) === 3}
            <div class="black note g {highlightNote(note.data, rangeStartNoteR, rangeStartNoteL)}" />
        {:else if (note.id % 12) === 4}
            <div class="white note g {highlightNote(note.data, rangeStartNoteR, rangeStartNoteL)}" />
        {:else if (note.id % 12) === 5}    
            <div class="white note {highlightNote(note.data, rangeStartNoteR, rangeStartNoteL)}" />
        {:else if (note.id % 12) === 6}
            <div class="black note g {highlightNote(note.data, rangeStartNoteR, rangeStartNoteL)}" />
        {:else if (note.id % 12) === 7}
            <div class="white note g {highlightNote(note.data, rangeStartNoteR, rangeStartNoteL)}" /> 
        {:else if (note.id % 12) === 8}
            <div class="black note g {highlightNote(note.data, rangeStartNoteR, rangeStartNoteL)}" />
        {:else if (note.id % 12) === 9}
            <div class="white note g {highlightNote(note.data, rangeStartNoteR, rangeStartNoteL)}" />
        {:else if (note.id % 12) === 10}
            <div class="black note g {highlightNote(note.data, rangeStartNoteR, rangeStartNoteL)}" />
        {:else}
            <div class="white note g {highlightNote(note.data, rangeStartNoteR, rangeStartNoteL)}" /> 
        {/if}
    {/each}
    
</div>
<button on:click={handleonclick}> click me </button>

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
    .highlight-red {
        background-color: red;
        border-left: 1px solid black;
		border-bottom: 1px solid black;
    }
    .g {
        margin:0 0 0 -0.5em
    }
</style>

