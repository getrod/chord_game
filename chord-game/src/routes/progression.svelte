<script>
	import ChordSequence from '../component/ChordSequence.svelte';
	import { chordGeneratorRandom } from '../lib/ChordSequence.svelte';
	import { getChordProgression, addKeysToChordSequence } from '../lib/ChordProression.svelte';
	import { chordMatch } from '../lib/Chord.svelte';
	import ActiveNotes from '../lib/ActiveNotes.svelte';
    import { flip } from 'svelte/animate';

	$: chordSequence = [];
	let notes = [];
	let chordProgStr = '[1]-maj [4]-maj [5]-maj';
	let keysStr = '0';
	let playGame = false;
	let scorePage = false;
    let startTime
    let chordPerMin = 0
    let score = 0
    let elapsedTimes = []

	function handlePlayGame(e) {
		chordSequence = [];
		let keys = keysStr.split(',');
		keys.forEach((key) => {
			let chords = getChordProgression(chordProgStr, parseInt(key));
			chordSequence = chordSequence.concat(chords);
		});
        addKeysToChordSequence(chordSequence)

        playGame = true
        scorePage = false

        startTime = Date.now()
        chordPerMin = 0
        score = 0
        console.log(chordSequence)
	}

    function handleNewGame() {
        scorePage = false
    }

	function handleNoteEvent(e) {
		// if sequence over, go to score page
		if (chordSequence.length === 0) {
            scorePage = true
            playGame = false
            return;
        }

		notes = e.detail.activeNotes;
		if (chordMatch(notes, chordSequence[0].name)) {
			chordSequence = chordSequence.slice(1);
			score += 10;

            let elapsed = Date.now() - startTime
            if (elapsed < 60 * 1000) { // if elapsed time less than 60 seconds
                elapsedTimes.push(elapsed)
                let sum = elapsedTimes.reduce((prev, t) => prev + t, 0) / 1000
                let averageElapse = sum / elapsedTimes.length
                console.log(`averageElapse: ${averageElapse}`)
                chordPerMin = (1/averageElapse) * 60 // chord/secs * secs/minutes
                console.log(`cpm: ${chordPerMin}`)
                startTime = Date.now()
            }
		}
	}
</script>

{#if playGame}
	<ActiveNotes on:note={handleNoteEvent} />
	<h1>Chord Progression</h1>
	<div style="display: flex; ">
		{#each chordSequence as chord, i (chord.id)}
			<div animate:flip class="chord-card" style={i === 0 ? 'background-color: green;' : ''}>
				<p class="chord-text" style={i === 0 ? 'color: white;' : ''}>{chord.name}</p>
			</div>
		{/each}
	</div>
{:else if scorePage}
	<h1>Score: {score}</h1>
    <h1>CPM: {Math.floor(chordPerMin)}</h1>
    <button on:click={handleNewGame}>New Game</button>
{:else}
	<h1>Chord Progression Settings</h1>
	<form class="content">
		<label for="prog">Progression Formula</label>
		<input type="text" bind:value={chordProgStr} placeholder="ex: [1]-maj [4]-maj [5]-maj" />
		<label for="prog">Keys</label>
		<input type="text" bind:value={keysStr} placeholder="ex: 0 for key 'C'" />
	</form>
	<button on:click={handlePlayGame}>Play Game</button>
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
		padding: 0 10px 0 10px ;
	}
</style>
