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

if __name__ == '__main__':
    unittest.main()