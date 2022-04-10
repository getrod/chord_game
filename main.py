from __future__ import print_function

import logging
import sys
import time

from rtmidi.midiutil import open_midiinput

from midi_provider import midi_provider
from instrument import *
from chord_interpreter import *
from client import ChordClient

log = logging.getLogger('midiin_callback')
logging.basicConfig(level=logging.DEBUG)

try:
    midiin, port_name = open_midiinput()
except (EOFError, KeyboardInterrupt):
    sys.exit()

instrument = Instrument()
midi_provider.subscribe(instrument)
chord_interpreter = ChordInterpreter(instrument)
client = ChordClient(chord_interpreter)

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