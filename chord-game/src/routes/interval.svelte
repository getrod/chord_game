<script>
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
	import { chordMatch, noteName } from '../lib/Chord.svelte';
	import { chordGeneratorRandom } from '../lib/ChordSequence.svelte';
	import ActiveNotes from '../lib/ActiveNotes.svelte';
	import { onMount } from 'svelte';
	import { addKeysToArray } from '../lib/Util.svelte';
	import { tweened } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';

	const progress = tweened(0, {
		duration: 400,
		easing: cubicOut
	});

	const timerProgress = tweened(0, {
		duration: 400,
		easing: cubicOut
	});

	let lowestNote = 36;
	let highestNote = 96;
	const intervalRange = 20;
	let rangeStartNote = 60;
	let chord = '';
	let score = 0;
	const randomNumSuccess = () => Math.floor(Math.random() * 5) + 5; // 5-10
	let numSuccess = randomNumSuccess();
	let successCounter = numSuccess;
	let jumpSpeed = 3;
	let direction = jumpSpeed;
	let keyboardNotes = [];
	let activeNotes = [];
	let timerInterval = 1000;
	let gameTime = 3 * 60 * timerInterval; // 3 minutes
	let timerCounter = 0;
	let timerString = '';

	let chordFilterStr = '';
	let keyFilterStr = '';
    let keyFilter = [];
    let chordFilter = [];
	let gameStart = false;
    let scorePage = false
    let intervalFunc

	onMount(() => {
		for (let i = lowestNote; i <= highestNote; i++) {
			keyboardNotes.push(i);
		}
		keyboardNotes = addKeysToArray(keyboardNotes);
	});

	function handlePlayGame() {
		chordFilter = chordFilterStr.replace(/\s+/g, '').split(',');
		keyFilter = keyFilterStr.replace(/\s+/g, '').split(',');
		keyFilter.forEach((key, index) => (keyFilter[index] = noteName(key)));

		if (chordFilterStr.trim() === '') chordFilter = null;
		if (keyFilterStr.trim() === '') keyFilter = null;

		chord = chordGeneratorRandom(1, keyFilter, chordFilter)[0];
		gameStart = true;
        timerString = '';
        timerCounter = 0;
        timerProgress.set(0)
        progress.set(0);
        score = 0

        if (intervalFunc) {
            clearInterval(intervalFunc)
        }

		intervalFunc = setInterval(() => {
			timerProgress.set(timerCounter / gameTime);
			timerCounter += timerInterval;
			let totalSeconds = timerCounter / 1000;
			let minutes = Math.floor(totalSeconds / 60);
			let seconds = Math.floor(totalSeconds) % 60;

			timerString = `${minutes}:${seconds.toString().padStart(2, '0')}`;
            if (timerCounter >= gameTime) {
                clearInterval(intervalFunc)
                scorePage = true
                gameStart = false
                
            }
		}, timerInterval);
	}

	function noteInRange(note, startNote) {
		return note >= startNote && note < startNote + intervalRange;
	}

	function highlightNote(note, startNote, activeNotes) {
		if (activeNotes.includes(note)) {
			return 'highlight-red';
		}
		if (noteInRange(note, startNote)) {
			return 'highlight';
		}
	}

	function handleOnNote(e) {
        if (!gameStart) return
		activeNotes = Array.from(e.detail.activeNotes);
		let validRange = true;
		activeNotes.forEach((note) => {
			validRange = validRange && noteInRange(note, rangeStartNote);
		});

		if (!validRange) {
			return;
		}

		if (chordMatch(activeNotes, chord)) {
			// add to some score
			score += 10;

			// nudge the interval range
			if (rangeStartNote <= lowestNote) {
				direction = jumpSpeed;
			} else if (rangeStartNote + intervalRange >= highestNote) {
				direction = -1 * jumpSpeed;
			}

			rangeStartNote += direction;

			successCounter--;
			if (successCounter === 0) {
				// get new chord
				chord = chordGeneratorRandom(1, keyFilter, chordFilter)[0];
				numSuccess = randomNumSuccess();
				successCounter = numSuccess;
			}
			console.log(successCounter);
			progress.set((numSuccess - successCounter) / numSuccess);
		}
	}
</script>

{#if gameStart}
	<div style="display: flex; justify-content: space-between; padding: 0 20% 10px 20%">
		<span><h1 class="chord">{chord}</h1> <p>{successCounter}</p> </span>
		<h1>Score {score}</h1>
	</div>
	<ActiveNotes on:note={handleOnNote} />
	<div style="padding: 0 20% 10px 20%">
		<progress value={$progress} />
	</div>
	<div class="keys">
		{#each keyboardNotes as note (note.id)}
			{#if note.id % 12 === 0}
				<div class="white note {highlightNote(note.data, rangeStartNote, activeNotes)}" />
			{:else if note.id % 12 === 1}
				<div class="black note g {highlightNote(note.data, rangeStartNote, activeNotes)}" />
			{:else if note.id % 12 === 2}
				<div class="white note g {highlightNote(note.data, rangeStartNote, activeNotes)}" />
			{:else if note.id % 12 === 3}
				<div class="black note g {highlightNote(note.data, rangeStartNote, activeNotes)}" />
			{:else if note.id % 12 === 4}
				<div class="white note g {highlightNote(note.data, rangeStartNote, activeNotes)}" />
			{:else if note.id % 12 === 5}
				<div class="white note {highlightNote(note.data, rangeStartNote, activeNotes)}" />
			{:else if note.id % 12 === 6}
				<div class="black note g {highlightNote(note.data, rangeStartNote, activeNotes)}" />
			{:else if note.id % 12 === 7}
				<div class="white note g {highlightNote(note.data, rangeStartNote, activeNotes)}" />
			{:else if note.id % 12 === 8}
				<div class="black note g {highlightNote(note.data, rangeStartNote, activeNotes)}" />
			{:else if note.id % 12 === 9}
				<div class="white note g {highlightNote(note.data, rangeStartNote, activeNotes)}" />
			{:else if note.id % 12 === 10}
				<div class="black note g {highlightNote(note.data, rangeStartNote, activeNotes)}" />
			{:else}
				<div class="white note g {highlightNote(note.data, rangeStartNote, activeNotes)}" />
			{/if}
		{/each}
	</div>
	<div style="padding: 10px 10% 10px 10%; text-align: center;">
		<progress value={$timerProgress} />
		<h1>{timerString}</h1>
	</div>
{:else if scorePage}
    <h1 class="score">Score: {score}</h1>
    <button on:click={() => scorePage = false}> New Game </button>
{:else}
	<h2>Filters</h2>
	<p>Leave empty to play all defined chords</p>
	<form>
		<label for="prog">Chord Filter</label>
		<input type="text" bind:value={chordFilterStr} placeholder="ex: maj, m, m9, etc." />
		<label for="prog">Key Filter</label>
		<input type="text" bind:value={keyFilterStr} placeholder="ex: 0, 2, 5 for 'C, D, F'" />
	</form>
	<button on:click={handlePlayGame}> Play Game </button>
{/if}

<style>
	.keys {
		position: relative;
		padding: 0 5% 0 5%;
	}
	.keys div:last-child {
		border-right: 0.7px solid #bbb;
	}
	.note {
		position: relative;
		float: left;
		padding: 0;
		margin: 0;
	}
	.white {
		height: 8em;
		width: 2em;
		z-index: 1;
		position: relative;
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
		margin: 0 0 0 -0.5em;
	}
	progress {
		display: block;
		width: 100%;
	}
	.chord {
		font-size: 5rem;
		text-align: center;
		padding: 0;
		margin: 0;
	}
    .score {
        font-size: 5rem;
		padding: 0;
		margin: 0;
    }
    
</style>
