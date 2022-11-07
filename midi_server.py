from __future__ import print_function

import socketio
import fluidsynth
import time
import sys
from rtmidi import (midiutil, MidiIn, midiconstants)

sio = socketio.Client()
fs = fluidsynth.Synth()

def start_synth():
    fs.start()
    dir = 'sound_fonts'
    sfid = fs.sfload(f'{dir}/Nice-Steinway-Lite-v3.0.sf2')
    fs.program_select(0, sfid, 0, 0)

def play_midi(midi):
    if midi['midi_event'] == 'note_on':
        fs.noteon(0, midi['note'], midi['velocity'])
    else:
        fs.noteoff(0, midi['note'])        

def midi_callback(event, data=None):
    message, deltatime = event
    if message[0] == midiconstants.NOTE_ON \
    and message[2] != 0:
        midi_event = 'note_on'
    else:
        midi_event = 'note_off'

    midi = {
        'midi_event': midi_event,
        'note': message[1],
        'velocity': message[2]
    }

    play_midi(midi)
    sio.emit('midi_event', midi)


def start():
    midiin = MidiIn()
    
    ''' socket callbacks '''
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

    ''' open midi input '''
    try:
        midiin, port_name = midiutil.open_midiinput()
    except (EOFError, KeyboardInterrupt):
        sys.exit()
    midiin.set_callback(midi_callback) 

    ''' connect socket '''
    sio.connect('http://localhost:3000')

    ''' start synth '''
    start_synth()

    print("Entering main loop. Press Control-C to exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('')
    finally:
        print("Exit.")
        midiin.close_port()
        fs.delete()
        del midiin


start()