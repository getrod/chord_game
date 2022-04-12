import music21 as m21
import random

chord_types = [
    {
        'name': 'maj',
        'formula': {'1', '3', '5'},
    },
    {
        'name': 'm',
        'formula': {'1', 'b3', '5'},
    },
    {
        'name': 'sus2',
        'formula': {'1', '2', '5'},
    },
    {
        'name': 'sus4',
        'formula': {'1', '4', '5'},
    },
    {
        'name': 'maj7',
        'formula': {'1', '3', '5', '7'},
    },
    {
        'name': '7',
        'formula': {'1', '3', '5', 'b7'},
    },
    {
        'name': 'm7',
        'formula': {'1', 'b3', '5', 'b7'},
    },
    {
        'name': 'maj add2',
        'alt': 'maj add9',
        'formula': {'1', '2', '3', '5'},
    },
    {
        'name': 'm add2',
        'alt': 'm add9',
        'formula': {'1', '2', 'b3', '5'},
    },
    {
        'name': 'maj9',
        'formula': {'1', '2', '3', '5', '7'},
    },
]



voice_rules = [
    # TRIADS
    {
        'name': 'root',
        'details': 'triad',
        'voice': [1, 2, 3]
    },
    {
        'name': '1st inv',
        'details': 'triad',
        'voice': [2, 3, 1]
    },
    {
        'name': '2nd inv',
        'details': 'triad',
        'voice': [3, 1, 2]
    },

    # TETRAD
    {
        'name': 'root',
        'details': 'tetrad',
        'voice': [1, 2, 3, 4]
    },
    {
        'name': '1st inv',
        'details': 'tetrad',
        'voice': [2, 3, 4, 1]
    },
    {
        'name': '2nd inv',
        'details': 'tetrad',
        'voice': [3, 4, 1, 2]
    },
    {
        'name': '3rd inv',
        'details': 'tetrad',
        'voice': [4, 1, 2, 3]
    },
]

note_names =    [m21.note.Note('C'), m21.note.Note('C#'), m21.note.Note('D'), 
                m21.note.Note('E-'), m21.note.Note('E'), m21.note.Note('F'), 
                m21.note.Note('F#'), m21.note.Note('G'), m21.note.Note('G#'), 
                m21.note.Note('A'), m21.note.Note('B-'), m21.note.Note('B')]
note_numbers =  ['1', 'b2', '2', 'b3', '3', '4', 'b5', '5', '#5', '6', 'b7', '7']

note_num_sort_key = lambda note_num: note_numbers.index(note_num)
note_sort_key = lambda note: note.pitches[0].midi

def findVoiceRule(voice : list[int]) -> dict:
    for voice_rule in voice_rules:
        if voice_rule['voice'] == voice:
            return voice_rule
    return None

def findChordVoicing(key: str, chord_type: dict, notes: list[m21.note.Note]) -> dict:
    # sort the notes by their position on the keyboard
    notes.sort(key=note_sort_key)

    # turn sorted notes into list of note numbers
    note_numbers = []
    for note in notes:
        note_numbers.append(noteToNumber(key=key, note=note.name))

    # turn the note numbers list into list of index of the chord formula
    chord_form_list = formulaListSorted(chord_type)
    voice = []
    for note_number in note_numbers:
        voice.append(chord_form_list.index(note_number) + 1)

    return findVoiceRule(voice)


def noteIdx(note):
    note_ = m21.note.Note(note.name)
    return note_names.index(note_)

def formulaListSorted(chord_type) -> list[str]:
    return list(sorted(chord_type['formula'], key=note_num_sort_key))

def ruleToString(rule):
    for rule_ in chord_types:
        print(str(type(rule_)))
        if rule_['name'] == rule['name']:
            return '{' + 'name: ' + rule_['name'] + ', ' + 'form: ' \
                + str(sorted(rule_['formula'], key=note_num_sort_key)) + '}'

def numbersToChordType(note_numbers):
    chord_formula = set(note_numbers)
    for chord_type in chord_types:
        if chord_type['formula'] == chord_formula:
            return chord_type
    return None

def numberToNote(key: str, number: str): 
    key_ = m21.note.Note(key)
    offset = note_names.index(key_)
    number_idx = note_numbers.index(number)    
    return note_names[(number_idx - offset) % len(note_names)]

# get notes from key and chord numbers
def numbersToNotes(key, numbers: set[str]):
    notes = []
    for number in numbers:
        notes.append(numberToNote(key, number).name)
    return notes

def noteToNumber(key, note):
    key_ = m21.note.Note(key)
    note_ = m21.note.Note(note)
    offset = note_names.index(key_)
    note_idx = note_names.index(note_)
    return note_numbers[(note_idx - offset) % len(note_numbers)]


def notesToNumbers(key, notes):
    note_num_set = set()
    for note in notes:
        note_num_set.add(noteToNumber(key, note))   
    return sorted(note_num_set, key=note_num_sort_key)

def Chord(key: str, notes: list[str], type: dict = None, voice: dict = None):
    chord = {
        'key': key,
        'notes': notes
    }

    if type:
        chord['type'] = type

    if voice:
        chord['voice'] = voice
    return chord

def findChordType(key, notes: set[str]):
    note_nums = notesToNumbers(key, notes)
    chord_type = numbersToChordType(note_nums)
    return chord_type

# for each potential key, find a chord rule
def findChordsAmbiguous(notes: list[m21.note.Note]) -> list[dict]:
    chords = []
    note_names = set(map(lambda note: note.name, notes))
    sorted_notes = list(map(lambda note: note.nameWithOctave, sorted(notes, key=note_sort_key)))
    for key in note_names:
        chord_type = findChordType(key=key, notes=note_names)
        if chord_type != None:
            # get voicing
            voice = findChordVoicing(key=key, chord_type=chord_type, notes=notes)
            chords.append(Chord(key=key, notes=sorted_notes, type=chord_type, voice=voice))
    if len(chords) > 0:
        return chords
    return [Chord(key=None, notes=sorted_notes)]

def chordToString(chord: dict):
    if chord['key']:
        s = chord['key'] + chord['type']['name']
        if 'voice' in chord:
            s += ' (' + chord['voice']['name'] + ')'
        return s
    return str(chord['notes'])  


def chordsToString(chords: list[dict]):
    s = ''
    for chord in chords:
        s += chordToString(chord) + ' |'
    if s != '': return s[:-1]
    return s
        

def getRandomChord(voice=False):
    key = random.choice(note_names).name
    chord_type = random.choice(chord_types)
    voice_rule = None
    if voice:
        # get size of chord formula
        size = len(chord_type['formula'])
        # make an array of voices with that size (ie. 3 for trias)
        filtered_voices = list(filter(lambda voice: len(voice['voice']) == size, voice_rules))
        if len(filtered_voices) == 0:
            voice_rule = None
        else:
            # out of that filtered voice array, randomly choose a voice
            voice_rule = random.choice(filtered_voices)
    notes = numbersToNotes(key, chord_type['formula'])
    return Chord(key=key, notes=notes, type=chord_type, voice=voice_rule)

# combine: { major, minor } & { add2, add6, add9 } 
# Note to self: What I'm looking for in this file is 
# called "chord spelling". Here is an example link
# https://www.brendanpauljacobs.com/spelling.htm

'''

I wont have two definitions for the same chord type (ie. add2 & add9),
Instead, I'll just keep an alternate name in the chord type
https://music.stackexchange.com/questions/10990/chord-naming-conventions-add2-versus-add9/26761#26761


'''