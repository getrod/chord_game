from __future__ import print_function

import logging
import socketio
import time
import sys
from rtmidi import (midiutil, MidiIn)

log = logging.getLogger('midiin_callback')
logging.basicConfig(level=logging.DEBUG)

sio = socketio.Client()
midiin = MidiIn()
        
def midi_callback(event, data=None):
    message, deltatime = event
    print(message)
    sio.emit('midi_event', message)

sio.on('get_midi_ports')
def on_get_midi_ports():
    print('get_midi_ports')
    sio.emit('midi_ports', midiin.get_ports())

sio.on('select_midi_port')
def on_select_midi_port(port):
    print(f'select_midi_port: {port}')
    midiin, port_name = midiutil.open_midiinput(port)
    midiin.set_callback(midi_callback) 
    sio.emit('is_port_open', midiin.is_port_open())

try:
    midiin, port_name = midiutil.open_midiinput(0)
except (EOFError, KeyboardInterrupt):
    sys.exit()

midiin.set_callback(midi_callback) 
sio.connect('http://localhost:3000')

print("Entering main loop. Press Control-C to exit.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('')
finally:
    print("Exit.")
    midiin.close_port()
    del midiin