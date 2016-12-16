import unittest
from stem import Stemmer
import bulgarian_stems

class TestStemmer(unittest.TestCase):
    def test_bulgarian(self):
        test_cases(self, bulgarian_stems.STEMS, 'bulgarian.pl', 'bulgarian_words')

def test_cases(test, stems, rules_file, dict_file):
    stemmer = Stemmer(rules_file, dict_file)
    for stem, cases in stems:
        for case in cases:
            test.assertEqual(list(stemmer([case]))[0], stem)

if __name__ == '__main__':
    unittest.main()
