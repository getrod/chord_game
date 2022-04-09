import music21 as m21
from observer import *
from instrument import Instrument
from chord_rules import *


class ChordInterpreter(Listener):
    def __init__(self, instrument : Instrument):
        self.instrument = instrument
        # subscribe to the instrument 
        # for state changes
        self.instrument.subscribe(self)


    def on_callback(self, message):
        notes = []
        note_names = set()
        for midi_note in message:
            note = m21.note.Note(midi_note)
            notes.append(note)
            note_names.add(note.name)
        
        # ## NEED
        # key = 'c'
        # chord_rule = chord_rules[0] # maj


        # # sort the notes by their position on the keyboard
        # notes.sort(key=lambda note: note.pitches[0].midi)

        # # turn sorted notes into list of note numbers
        # note_numbers = []
        # for note in notes:
        #     note_numbers.append(noteNumber(key=key, note=note.name))
        # print(note_numbers)

        # # turn the note numbers list into list of index of the chord rule
        # chord_form_list = formulaListSorted(chord_rule)
        # print(chord_form_list)
        # voice = []
        # for note_number in note_numbers:
        #     voice.append(chord_form_list.index(note_number) + 1)
        # print(voice)
        # print(findVoiceRule(voice))
        # # add 1 to each element of the array

        # return that array

        # for note in notes:
        #     print(note.nameWithOctave, end=', ')
        # print()

        
        
        chords = findChordsAmbiguous(notes)
        if len(chords) > 0:
            print(chordsToString(chords))
        

        
        # numbers_res = notesToNumbers('c' , note_names) # TODO: Change this assumption
        
        # print("Numbers: " + str(numbers_res))  
        # find chord rule to match note numbers
        # rules = findRules(numbers_res)
        # if len(rules) > 0:
        #     print(ruleToString(rules[0]))
    


print(noteNumber(key='F', note='F'))
