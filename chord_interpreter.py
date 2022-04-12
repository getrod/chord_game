import music21 as m21
from observer import *
from instrument import Instrument
from chord_rules import *


class ChordInterpreter(Listener, Provider):
    def __init__(self, instrument : Instrument):
        self.instrument = instrument
        # subscribe to the instrument 
        # for state changes
        self.instrument.subscribe(self)
        super().__init__()


    def on_callback(self, message):
        notes = []
        note_names = set()
        for midi_note in message:
            note = m21.note.Note(midi_note)
            notes.append(note)
            note_names.add(note.name)

        # print(getRandomChord(True))
        
        
        chords = findChordsAmbiguous(notes)
        if len(chords) > 0:
            print(chordsToString(chords))
        
        self.update_listeners(chords)
    
