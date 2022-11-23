import motif_compiler as motif
import unittest

class TestMotifCompiler(unittest.TestCase):
    def test_parse_key(self):
        key, i = motif.parse_key('Am9', 0)
        self.assertEqual(key, 'A')
        self.assertEqual(i, 1)
        key, i = motif.parse_key('A#m9', 0)
        self.assertEqual(key, 'A#')
        self.assertEqual(i, 2)
        key, i = motif.parse_key('Abm9', 0)
        self.assertEqual(key, 'Ab')
        self.assertEqual(i, 2)

        # check for space
        key, i = motif.parse_key(' Am9', 0)
        self.assertEqual(key, 'A')
        self.assertEqual(i, 2)

        # ensure assertion is raised
        self.assertRaises(Exception, motif.parse_key, 'H', 0)

    def test_parse_chord(self):
        chord, pos = motif.parse_chord('maj9', 0)
        self.assertEqual(chord, 'maj9')
        self.assertEqual(pos, 4)

        chord, pos = motif.parse_chord('maj9 ', 0)
        self.assertEqual(chord, 'maj9')
        self.assertEqual(pos, 4)

        # skip space test
        chord, pos = motif.parse_chord(' maj9 ', 0, True)
        self.assertEqual(chord, 'maj9')
        self.assertEqual(pos, 5)

        # the "sus" case
        self.assertRaises(Exception, motif.parse_chord, 'sus', 0)

        # other exceptions
        self.assertRaises(Exception, motif.parse_chord, 'a', 0)

    def test_parse_duration(self):
        self.assertEqual(motif.parse_duration('3/2'), 1.5)
        self.assertEqual(motif.parse_duration('1/2'), 0.5)
        self.assertEqual(motif.parse_duration('0'), 0)
        self.assertEqual(motif.parse_duration('4'), 4)

        # negative duration test
        self.assertRaises(Exception, motif.parse_duration, '-1/2')

    def test_parse_motif(self):
        test = '''Am9[3 4 5 6 7 | 3]-(3/2), B#m7[3 4 5 6 | 3]-(3/2), 
        Em7<[3 5]-(3/4), [6]-(1/4), [7 9]-(1/4), [8]-(1/4), [6]-(1/4) | 4>
        '''
        motifs = motif.parse_motif(test)
        self.assertEqual(motifs[0].key, 'A')
        self.assertEqual(motifs[0].chord_type, 'm9')
        self.assertEqual(motifs[0].notes, [3, 4, 5, 6, 7])
        self.assertEqual(motifs[0].duration, 1.5)
        self.assertEqual(motifs[0].octave, 3)

        self.assertEqual(motifs[1].key, 'B#')
        self.assertEqual(motifs[1].chord_type, 'm7')
        self.assertEqual(motifs[1].notes, [3, 4, 5, 6])
        self.assertEqual(motifs[1].duration, 1.5)
        self.assertEqual(motifs[1].octave, 3)

        self.assertEqual(motifs[2].key, 'E')
        self.assertEqual(motifs[2].chord_type, 'm7')
        self.assertEqual(motifs[2].note_seq, [[3, 5], [6], [7, 9], [8], [6]])
        self.assertEqual(motifs[2].duration_seq, [3/4, 1/4, 1/4, 1/4, 1/4])
        self.assertEqual(motifs[2].octave, 4)



if __name__ == '__main__':
    unittest.main()