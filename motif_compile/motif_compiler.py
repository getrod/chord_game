import re
'''
Example motif:
Am9[3 4 5 6 7 | 3]-(3/2), Bm7[3 4 5 6 | 3]-(3/2), Cmaj9[0 1 2 3 4 | 5]-(3/2), 
Em7<[3 5]-(3/4), [6]-(1/4), [7 9]-(1/4), [8]-(1/4), [6]-(1/4) | 4>,
Em7<[3]-(1/4), [2]-(1/4), [3]-(1/4), [4]-(1/4), [1]-(1/4) | 4>,
Em7[1 2 3 4 | 4]-(3/2),
Cmaj9[0 1 2 3 4 | 5]-(5/2),
Bm7[3 4 5 6 | 3]-(3/2),
Am9[3 4 5 6 7 | 3]-(3/2)


Syntax tree:
    List
        Chord
            Key: A -> number 9
            Type: m9
            Notes: [3, 4, 5, 6, 7]
            Octave?: 3
            Duration: 3/2
        Chord
            Key: B -> number 11
            Type: m7
            Notes: [3, 4, 5, 6]
            Octave?: 3
            Duration: 3/2
        Chord
            Key: C -> number 0
            Type: maj9
            Notes: [0, 1, 2, 3, 4]
            Octave?: 5
            Duration: 3/2
        BrokenChord
            Key: E -> number 4
            Type: m7
            Octave?: 4
            Note Sequence: [[3, 5], [6], [7, 9], [8], [6]]
            DurationSequence: [¾, ¼, ¼, ¼, ¼]
        BrokenChord
            Key: E -> number 4
            Type: m7
            Octave?: 4
            NoteSequence: [[3], [2], [3], [4], [1]]
            DurationSequence: [¼, ¼, ¼, ¼, ¼]
        ...
'''

base_keys = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
symbols = ['b', '#']

chord_names = ['maj', 'm', 'sus2', 'sus4', 'maj7', 'm7', 'maj9', 'm9']

''' returns the parsed key and ending search position'''
def parse_key(s: str, start: int) -> tuple[str, int]:
    state = 0
    i = start
    parsed_key = ''

    while i < len(s):
        if state == 0:
            # skip blank space at beginning
            if s[i].isspace(): i += 1
            else: state = 1
        if state == 1:
            # Is first char a base key?
            if s[i] in base_keys: 
                parsed_key += s[i]
                i += 1
                state = 2
            else: raise Exception(f'{s[i]} is not a defined base key.')
        elif state == 2:
            # Is next char a symbol?
            if s[i] in symbols:
                parsed_key += s[i]
                i += 1
            break
    return (parsed_key, i)

class Node:
    def __init__(self, value, is_terminal = False) -> None:
        self.value = value
        self.is_terminal = is_terminal
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)

    def has_child(self, child):
        return child in self.children
    
    ''' returns child with first value '''
    def find_child(self, value):
        for child in self.children:
            if child.value == value:
                return child
        return None

class ChordNameTree:
    def __init__(self):
        init_node = Node(-1)

        # make tree
        for chord_name in chord_names:
            current_node = init_node
            for char in chord_name:
                child = current_node.find_child(char)
                if child:
                    current_node = child
                else: 
                    node = Node(char)
                    current_node.add_child(node)
                    current_node = node
            current_node.is_terminal = True

        self.init_node = init_node

    def validate_input(self, s: str) -> bool:
        current_node = self.init_node
        for char in s:
            node = current_node.find_child(char)
            if node == None: return False
            current_node = node
            
        return current_node.is_terminal

    ''' Finds the first best match of the chord in the string '''
    def parse_chord(self, s: str, start: int, use_space=True) -> tuple[str,int]:
        current_node = self.init_node
        _parsed_chord = ''
        _start = start
        
        if use_space:
            # skip space in beginning
            for i in range(start, len(s)):
                if s[i].isspace() == False: 
                    _start = i
                    break
        
        _saved_chord = None
        _saved_pos = 0
        for i in range(_start, len(s)):
            char = s[i]
            node = current_node.find_child(char)
            if node == None:
                _parsed_chord += char # for the error message
                break 
            _parsed_chord += char
            if node.is_terminal:
                _saved_chord = _parsed_chord
                _saved_pos = i + 1
            current_node = node
        
        if _saved_chord: return (_saved_chord, _saved_pos)
        else: raise Exception(f'"{_parsed_chord if len(_parsed_chord) == 1 else _parsed_chord[:-1]}" is not a defined chord')

chord_tree = ChordNameTree()

''' returns the parsed chord and the ending search position '''
def parse_chord(s: str, start: int, use_space=False) -> tuple[str, int]:
    return chord_tree.parse_chord(s, start, use_space)

class CHORD_TYPE():
    CHORD = 'chord'
    BROKEN_CHORD = 'broken_chord'

class Chord:
    def __init__(self, key, chord_type, notes,  duration, octave = None):
        self.key = key
        self.chord_type = chord_type
        self.notes = notes
        self.duration = duration
        self.octave = octave
    
    def __str__(self) -> str:
        return f'Chord[key: {self.key}, chord: {self.chord_type}, notes: {self.notes}, duration: {self.duration}, octave: {self.octave}]'
    
    def toJSON(self):
        return {
            'type': CHORD_TYPE.CHORD,
            'key': self.key, 
            'chord_type': self.chord_type,
            'notes': self.notes,
            'duration': self.duration,
            'octave': self.octave
        }

class BrokenChord:
    def __init__(self, key, chord_type, note_seq, duration_seq, octave = None):
        self.key = key
        self.chord_type = chord_type
        self.note_seq = note_seq
        self.duration_seq = duration_seq
        self.octave = octave
    
    def __str__(self) -> str:
        return f'BrokenChord[key: {self.key}, chord: {self.chord_type}, note_seq: {self.note_seq}, duration_seq: {self.duration_seq}, octave: {self.octave}]'
    
    def toJSON(self):
        return {
            'type': str(CHORD_TYPE.BROKEN_CHORD),
            'key': self.key, 
            'chord_type': self.chord_type,
            'note_seq': self.note_seq,
            'duration_seq': self.duration_seq,
            'octave': self.octave
        }

def parse_keychord(keychord: str, strict = True):
    key, kpos = parse_key(keychord, 0)
    chord = ''
    cpos = -1
    try:
        chord, cpos = parse_chord(keychord, kpos)
    except Exception as err:
        if strict: raise err
    return key, kpos, chord, cpos

def parse_octave(octave_str: str):
    octave = None
    octave_str = octave_str.strip()
    if octave_str != '':
        try: 
            octave = int(octave_str)
        except ValueError: raise Exception(f'"{octave_str}" is an invalid octave.')
    return octave

def parse_chord_motif(s: str, start: int, strict = True):
    state = 0
    keychord_parsed = ''
    notes_parsed = ''
    duration_parsed = ''
    i = start
    valid = False
    e_message = 'empty chord'
    pos = -1

    ''' seperate the different strings to be parsed '''
    while i < len(s):
        char = s[i]
        # get keychord
        if state == 0:
            if char == '[': 
                state = 1
                i += 1
            else:
                keychord_parsed += char
                i += 1
            if i >= len(s):
                e_message = 'no "[" found'
                break
        # get notes
        elif state == 1:
            if char == ']':
                state = 2
                i += 1
            else:
                notes_parsed += char
                i += 1
            if i >= len(s):
                e_message = 'no "]" found'
                break
        # get duration
        elif state == 2:
            if char == '-':
                state = 3
                i += 1
            else: 
                e_message = f'no "-" found, got: {char}'
                break
        elif state == 3:
            if char == '(':
                state = 4
                i += 1
            else: 
                e_message = f'no "(" found, got: "{char}"'
                break
        elif state == 4:
            if char == ')':
                valid = True
                pos = i + 1
                break
            duration_parsed += char
            i += 1
            if i >= len(s):
                e_message = f'no ")" found'
                break
    if not valid: raise Exception(f'{e_message}')

    # print(f'keychord: "{keychord_parsed}", notes: "{notes_parsed}", duration: "{duration_parsed}"')

    ''' convert parsed strings into chord object '''
    key, kpos, chord, cpos = parse_keychord(keychord_parsed, False)
    
    
    if strict and cpos != len(keychord_parsed):
        raise Exception(f'"{keychord_parsed[kpos:]}" is not a defined chord')
    
    # notes
    octave = None
    if '|' in notes_parsed:
        notes_str, octave_str = notes_parsed.split('|')
        octave = parse_octave(octave_str)
    else: notes_str = notes_parsed
    notes = parse_notes(notes_str)

    # duration
    duration = parse_duration(duration_parsed)
    return Chord(key, chord, notes, duration, octave)
    

def parse_notes(s: str) -> list[int]:
    _s = s.strip()
    notes_str = _s.split(' ')
    notes = []
    for note_str in notes_str:
        try:
            note = int(note_str)
            notes.append(note)
        except ValueError: raise Exception(f'"{note_str}" is not a note number.')
    return notes
    
def parse_duration(s: str) -> float:
    tokens = s.split('/')
    try:
        val = int(tokens[0])
        for token in tokens[1:]:
            val /= float(int(token))
    except ValueError: raise Exception(f'{val} is not an int')

    # cant be negative
    if val < 0: raise Exception(f'duration cannot be negative, but got {val}')
    return val

def parse_motif(s: str):
    tokens = re.split('\s*,\s*', s)
    motif = []

    brokenchord_key = ''
    brokenchord_chord = ''
    brokenchord_notes = []
    brokenchord_durations = []
    parsing_brokenchord = False
    for token in tokens:
        token = token.strip()
        ''' broken chord case '''
        if '<' in token:
            brokenchord_keychord, chord_piece = token.split('<')
            key, _, chord, _ = parse_keychord(brokenchord_keychord)
            brokenchord_key = key
            brokenchord_chord = chord
            parsing_brokenchord = True
        elif '>' in token:
            _token = token.split('>')[0]
            _tokens = _token.split('|')
            chord_piece = _tokens[0]

            # last chord piece
            chord = parse_chord_motif(chord_piece, 0, False)
            brokenchord_notes.append(chord.notes)
            brokenchord_durations.append(chord.duration)

            # octave
            octave = None
            if len(_tokens) > 1:
                octave_str = _tokens[1]
                octave = parse_octave(octave_str)

            bc = BrokenChord(brokenchord_key, brokenchord_chord, brokenchord_notes, brokenchord_durations, octave)
            motif.append(bc)

            brokenchord_key = ''
            brokenchord_chord = ''
            brokenchord_notes = []
            brokenchord_durations = []
            parsing_brokenchord = False
            continue

        if parsing_brokenchord:
            chord = parse_chord_motif(token, 0, False)
            brokenchord_notes.append(chord.notes)
            brokenchord_durations.append(chord.duration)
            continue

        ''' chord case '''
        chord = parse_chord_motif(token, 0, True)
        motif.append(chord)
    return motif

def motif_to_json(motif):
    motif_json = []
    for chord in motif:
        motif_json.append(chord.toJSON())
    return motif_json