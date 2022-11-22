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
        chord, pos = motif.parse_chord(' maj9 ', 0)
        self.assertEqual(chord, 'maj9')
        self.assertEqual(pos, 5)

        # the "sus" case
        self.assertRaises(Exception, motif.parse_chord, 'sus', 0)

        # other exceptions
        self.assertRaises(Exception, motif.parse_chord, 'a', 0)




if __name__ == '__main__':
    unittest.main()