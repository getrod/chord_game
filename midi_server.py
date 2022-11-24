from __future__ import print_function

import socketio
import fluidsynth
import pyaudio
import numpy
import math
import time
import sys
from rtmidi import (midiutil, MidiIn, midiconstants)
from motif_compile.motif_compiler import parse_motif, motif_to_json
import threading 


pa = pyaudio.PyAudio()
sample_rate = 44100
channels = 2
strm = pa.open(
    format = pyaudio.paInt16,
    channels = channels, 
    rate = sample_rate, 
    output = True)

sio = socketio.Client()
fs = fluidsynth.Synth()
lock = threading.Lock()

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

def play_track(midi_events, bpm):
    
    _fs = fluidsynth.Synth()
    dir = 'sound_fonts'
    sfid = _fs.sfload(f'{dir}/Nice-Steinway-Lite-v3.0.sf2')
    _fs.program_select(0, sfid, 0, 0)

    ppq = 98
    secondsPerMinute = 60
    secondsPerBeat = (secondsPerMinute) / (bpm)
    seconds_per_tick = secondsPerBeat / ppq
    current_tick = 0
    prev_tick = -1

    

    class MidiEvent:
        def __init__(self, event, note, velocity, tick):
            self.event = event
            self.note = note
            self.velocity = velocity
            self.tick = tick

        def __str__(self) -> str:
            return '{' + f'event: {self.event}, note: {self.note}, velocity: {self.velocity}, tick: {self.tick}' \
            + '}'

    def midiEventsPrint(events):
        for event in events:
            print(event)

    def beat2Tick(beat):
        return  math.floor(beat * ppq)

    _midi_events = []
    for midi_event in midi_events:
        _midi_event = midi_event['midi_event']
        beat = midi_event['beat']
        event = 'on' if _midi_event['midi_event'] == 'note_on' else 'off'
        _midi_events.append(MidiEvent(event, _midi_event['note'], _midi_event['velocity'], beat2Tick(beat)))

    _midi_events.sort(key=lambda midi_event : midi_event.tick) # by tick time

    def activate_midi_event(midi_event):
        if midi_event.event == 'on':
            _fs.noteon(0, midi_event.note, midi_event.velocity)
        else:
            _fs.noteoff(0, midi_event.note)


    '''     Render Audio        '''
    s = []
    # Initial silence is 1 second
    s = numpy.append(s, _fs.get_samples(sample_rate * 1))

    while len(_midi_events) != 0:
        # find the first tick value that is greater than prev_tick 
        for i in range(0, len(_midi_events)):
            if _midi_events[i].tick > prev_tick:
                current_tick = _midi_events[i].tick 
                break
        if prev_tick < 0: prev_tick = 0

        print()
        
        # find all events in the current_tick
        same_tick_events = []
        while len(_midi_events) != 0:
            if _midi_events[0].tick == current_tick:
                same_tick_events.append(_midi_events.pop(0))
            else: break

        # render audio
        s = numpy.append(s, _fs.get_samples(math.floor(sample_rate * seconds_per_tick * (current_tick - prev_tick))))

        # activate midi events of current tick
        for midi_event in same_tick_events:
            activate_midi_event(midi_event)

        prev_tick = current_tick
    
    # End with silence 1 second
    s = numpy.append(s, _fs.get_samples(sample_rate * 1))

    _fs.delete()

    _s = []
    print (len(s))
    print ('Sending audio')
    int16_min = -32_768 
    int16_max = 32_767
    for sample in s:
        # normalize the sample
        norm_samp = ((sample + abs(int16_min)) / (abs(int16_min) + int16_max)) - 0.5
        _s.append(norm_samp)
    
    sio.emit('audio_event', {
        'audio_buffer': _s, 
        'sample_rate': sample_rate, 
        'num_channels': channels 
    })
    

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
    @sio.on('get_midi_ports')
    def on_get_midi_ports():
        print('get_midi_ports')
        sio.emit('midi_ports', midiin.get_ports())

    @sio.on('select_midi_port')
    def on_select_midi_port(port):
        print(f'select_midi_port: {port}')
        midiin, port_name = midiutil.open_midiinput(port)
        midiin.set_callback(midi_callback) 
        sio.emit('is_port_open', midiin.is_port_open())

    @sio.on('midi_track_event')
    def on_midi_track_event(midi_event):
        play_midi(midi_event)

    @sio.on('midi_track')
    def on_midi_track(track):
        print('called!')
        lock.acquire()
        play_track(track['track'], track['bpm'])
        lock.release()

    ### motif section

    @sio.on('motif_compile')
    def on_motif_compile(motif_string):
        print('yo Im being compiled')
        # print(motif_string)
        try:
            motif = parse_motif(motif_string)
            print('in try catch being parsed')
            motif_json = motif_to_json(motif)
            print('about to be sent with: "motif_compile_complete"')
            sio.emit('motif_compile_complete', motif_json)
        except Exception as e:
            print(e)
            sio.emit('motif_compile_error', str(e))   



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