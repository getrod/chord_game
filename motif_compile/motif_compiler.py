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
'''

ex = '''Am9[3, 4, 5, 6, 7 | 3]-(3/2), Bm7[3, 4, 5, 6 | 3]-(3/2), 
Cmaj9[0, 1, 2, 3, 4 | 5]-(3/2), 
Em7<[3, 5]-(3/4), [6]-(1/4), [7, 9]-(1/4), [8]-(1/4), [6]-(1/4) | 4>,
'''

base_keys = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
symbols = ['b', '#']

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
            else: raise Exception(f'{s[i]} is not a base key.')
        elif state == 2:
            # Is next char a symbol?
            if s[i] in symbols:
                parsed_key += s[i]
                i += 1
            return (parsed_key, i)


