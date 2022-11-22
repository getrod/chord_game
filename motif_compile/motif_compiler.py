'''
Am9[3, 4, 5, 6, 7 | 3]-(3/2), 
Bm7[3, 4, 5, 6 | 3]-(3/2), 
Cmaj9[0, 1, 2, 3, 4 | 5]-(3/2), 
Em7<[3, 5]-(3/4), [6]-(1/4), [7, 9]-(1/4), [8]-(1/4), [6]-(1/4) | 4>,
Em7<[3]-(1/4), [2]-(1/4), [3]-(1/4), [4]-(1/4), [1]-(1/4) | 4>,
Em7[1, 2, 3, 4 | 4]-(3/2),
Cmaj9[0, 1, 2, 3, 4 | 5]-(5/2),
Bm7[3, 4, 5, 6 | 3]-(3/2),
Am9[3, 4, 5, 6, 7 | 3]-(3/2)

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

Chord extensions: Am-add2[...], Bmaj7-add4[...]
'''

ex = '''Am9[3, 4, 5, 6, 7 | 3]-(3/2), Bm7[3, 4, 5, 6 | 3]-(3/2), 
Cmaj9[0, 1, 2, 3, 4 | 5]-(3/2), 
Em7<[3, 5]-(3/4), [6]-(1/4), [7, 9]-(1/4), [8]-(1/4), [6]-(1/4) | 4>,
'''

base_keys = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
symbols = ['b', '#']

chord_names = ['maj', 'm', 'sus2', 'sus4', 'maj7', 'm7', 'maj9', 'm9']
chord_ext = ['add2', 'add4']

''' returns the parsed key and ending search position'''
def parse_key(s: str, start: int) -> tuple[str, int]:
    state = 0
    i = start
    parsed_key = ''

    while True:
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
    def parse_chord(self, s: str, start: int) -> tuple[str,int]:
        current_node = self.init_node
        _parsed_chord = ''

        # skip space in beginning
        _start = start
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
        else: raise Exception(f'"{_parsed_chord}" is not a defined chord')

chord_tree = ChordNameTree()

''' returns the parsed chord and the ending search position '''
def parse_chord(s: str, start: int) -> tuple[str, int]:
    return chord_tree.parse_chord(s, start)

test_input = 'Ab maj9-add2'

# chord, pos = parse_chord("  pi ", 3)
# print(f'chord: {chord}, pos: {pos}')
key, pos = parse_key(test_input, 0)
chord, pos = parse_chord(test_input, pos)
print(f'key: {key}, chord: {chord}')