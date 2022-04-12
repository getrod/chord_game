from __future__ import print_function

import logging
import sys
import time

from rtmidi.midiutil import open_midiinput

from midi_provider import midi_provider
from instrument import *
from chord_interpreter import *
from client import ChordClient
from question import ChordQuestion
from validator import Validator
from chord_answer import ChordAnswer

log = logging.getLogger('midiin_callback')
logging.basicConfig(level=logging.DEBUG)


port = sys.argv[1] if len(sys.argv) > 1 else None

try:
    midiin, port_name = open_midiinput(port)
except (EOFError, KeyboardInterrupt):
    sys.exit()

instrument = Instrument()
midi_provider.subscribe(instrument)
chord_interpreter = ChordInterpreter(instrument)
# client = ChordClient(chord_interpreter)


chordQuestion = ChordQuestion()
# adds an 'a' infront of chord interpreter
# its a listener to chord interpreter, and a provider to validator
chordAnswer = ChordAnswer() 
chord_interpreter.subscribe(chordAnswer)

validator = Validator()
chordQuestion.subscribe(validator)
chordAnswer.subscribe(validator)

print("Attaching MIDI input callback handler.")
midi_provider.register_midiin(midiin, port_name)

# make a client that listens for midi evets

print("Entering main loop. Press Control-C to exit.")
try:
    # Just wait for keyboard interrupt,
    # everything else is handled via the input callback.
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('')
finally:
    print("Exit.")
    midiin.close_port()
    del midiin