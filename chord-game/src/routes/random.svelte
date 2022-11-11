<script>
	import ChordSequence from '../component/ChordSequence.svelte';
	import { chordGeneratorRandom } from '../lib/ChordSequence.svelte';
	import { getChordProgression, addKeysToChordSequence } from '../lib/ChordProression.svelte';
	import { chordMatch, noteName } from '../lib/Chord.svelte';
	import ActiveNotes from '../component/ActiveNotes.svelte';
	import { fade, fly } from 'svelte/transition';
	import { flip } from 'svelte/animate';
    import { tweened } from 'svelte/motion';
    import { cubicOut } from 'svelte/easing';


    const timerProgress = tweened(0, {
		duration: 400,
		easing: cubicOut
	});

	$: chordSequence = [];
	let score = 0;
	let notes = [];
	let chordFilterStr = '';
	let keyFilterStr = '';
	let lengthStr = '10';
	let chordFilter;
	let keyFilter;
	let gameStart = false;
	let scorePage = false;
	let infinite = false;
	let elapsedTimes = [];
	let startTime;
	let chordPerMin = 0;
    let timerCounter = 0;

	let intervalFunc;
    const timerInterval = 1000;
    let gameTime = 3 * 60 * timerInterval; // 3 minutes
    let timerString = '';

	function handlePlayGame() {
		chordFilter = chordFilterStr.replace(/\s+/g, '').split(',');
		keyFilter = keyFilterStr.replace(/\s+/g, '').split(',');
		keyFilter.forEach((key, index) => (keyFilter[index] = noteName(key)));

		if (chordFilterStr.trim() === '') chordFilter = null;
		if (keyFilterStr.trim() === '') keyFilter = null;
		let length = parseInt(lengthStr);
		if (isNaN(length)) {
			length = 10;
			infinite = true;
		} else {
			infinite = false;
		}

		chordSequence = chordGeneratorRandom(length, keyFilter, chordFilter);
		addKeysToChordSequence(chordSequence);
		score = 0;
		gameStart = true;
		scorePage = false;
		startTime = Date.now();
		chordPerMin = 0;
        timerCounter = 0;
        timerProgress.set(0)
        timerString = '';

		if (intervalFunc) {
			clearInterval(intervalFunc);
		}

		if (infinite) {
			intervalFunc = setInterval(() => {
				timerProgress.set(timerCounter / gameTime);
				timerCounter += timerInterval;
				let totalSeconds = timerCounter / 1000;
				let minutes = Math.floor(totalSeconds / 60);
				let seconds = Math.floor(totalSeconds) % 60;

				timerString = `${minutes}:${seconds.toString().padStart(2, '0')}`;
				if (timerCounter >= gameTime) {
					clearInterval(intervalFunc);
					scorePage = true;
					gameStart = false;
				}
			}, timerInterval);
		}
	}

	function handleNewGame() {
		gameStart = false;
        scorePage = false
	}

	function handleNoteEvent(e) {
        if (!gameStart) return
		// if sequence over, go to score page
		if (chordSequence.length === 0) {
			scorePage = true;
			gameStart = false;
			return;
		}

		notes = e.detail.activeNotes;
		if (chordMatch(notes, chordSequence[0].name)) {
			chordSequence = chordSequence.slice(1);
			if (infinite) {
				chordSequence.push({
					id: chordSequence[chordSequence.length - 1].id + 1,
					name: chordGeneratorRandom(1, keyFilter, chordFilter)[0]
				});
				console.log(chordSequence);
			}
			score += 10;

			let elapsed = Date.now() - startTime;
			if (elapsed < 60 * 1000) {
				// if elapsed time less than 60 seconds
				console.log(elapsed);
				elapsedTimes.push(elapsed);
				let sum = elapsedTimes.reduce((prev, t) => prev + t, 0) / 1000;
				let averageElapse = sum / elapsedTimes.length;
				console.log(`averageElapse: ${averageElapse}`);
				chordPerMin = (1 / averageElapse) * 60; // chord/secs * secs/minutes
				console.log(`cpm: ${chordPerMin}`);
				startTime = Date.now();
			}
		}
	}
</script>

{#if gameStart}
	<h1>Random Chord</h1>
	<div style="display: flex; justify-content: space-between;">
		<h1>Score: {score}</h1>
		<h1>CPM: {chordPerMin}</h1>
	</div>
	<button on:click={handleNewGame}> New Game </button>
	<ActiveNotes on:note={handleNoteEvent} />
	<div style="display: flex; ">
		{#each chordSequence as chord, i (chord.id)}
			<div animate:flip class="chord-card" style={i === 0 ? 'background-color: green;' : ''}>
				<p class="chord-text" style={i === 0 ? 'color: white;' : ''}>{chord.name}</p>
			</div>
		{/each}
	</div>
    {#if infinite}
    <div style="padding: 10px 10% 10px 10%; text-align: center;">
		<progress value={$timerProgress} />
		<h1>{timerString}</h1>
	</div>
    {/if}
{:else if scorePage}
	<h1>Random Chord</h1>
	<h1>Score: {score}</h1>
	<h1>Chords per minute (CMP): {Math.floor(chordPerMin)}</h1>
	<button on:click={handleNewGame}> New Game </button>
{:else}
	<h2>Filters</h2>
	<p>Leave key filter & chord filter empty to play all defined chords</p>
	<p>Leave Length empty to play an infine game of chords</p>
	<form class="content">
		<label for="prog">Chord Filter</label>
		<input type="text" bind:value={chordFilterStr} placeholder="ex: maj, m, m9, etc." />
		<label for="prog">Key Filter</label>
		<input type="text" bind:value={keyFilterStr} placeholder="ex: 0, 2, 5 for 'C, D, F'" />
		<label for="prog">Length</label>
		<input type="text" bind:value={lengthStr} />
	</form>
	<button on:click={handlePlayGame}> Play Game </button>
{/if}

<style>
	.content {
		display: grid;
		grid-column-gap: 10px;
		padding: 0% 20% 0% 0%;
	}
	.chord-card {
		border: 1px solid rgba(0, 0, 0, 0.1);
		box-shadow: 2px 4px 8px rgba(0, 0, 0, 0.1);
		border-radius: 5px;
		background-color: white;
		max-width: 20rem;
		max-height: 20rem;
		margin: 5px;
	}
	.chord-text {
		text-align: center;
		padding: 0 10px 0 10px;
	}
</style>
