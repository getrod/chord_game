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
from random_chord_game import RandomChordGame
from chord_numbers_game import ChordNumberGame
import my_socket

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


chord_number_game = ChordNumberGame()
chord_interpreter.subscribe(chord_number_game)

random_game = RandomChordGame()
chord_interpreter.subscribe(random_game)

@my_socket.sio.on('random game')
def on_random_game(data):
    print('now playing: random chord game')
    random_game.register_socket_handlers()

@my_socket.sio.on('number game')
def on_number_game(data):
    print('now playing: chord number game')
    chord_number_game.register_socket_handlers()

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