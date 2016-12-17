import unittest
import json
import os
from .stem import Stemmer
from . import bulgarian_stems

class Word:
    def __init__(self, text, word_type):
        self.text = text
        self.type = word_type

def load_dictionary(filename):
    with open(filename) as f:
        for subdictionary in json.load(f):
            word_type = subdictionary['type']
            for word in subdictionary['words']:
                yield Word(word, word_type)

class TestStemmer(unittest.TestCase):
    def test_bulgarian(self):
        test_cases(
            self,
            bulgarian_stems.STEMS,
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'bulgarian_grammar.pl'
            ),
            load_dictionary(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    'bulgarian_words.json'
                )
            )
        )

def test_cases(test, stems, rules_file, dict_file):
    stemmer = Stemmer(rules_file, dict_file)
    for stem, cases in stems:
        for case in cases:
            test.assertEqual(list(stemmer([case]))[0], stem)

if __name__ == '__main__':
    unittest.main()
