import unittest
import json
import os
from .stem import Stemmer, load_dictionary
from . import bulgarian_stems

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
    errors = []
    for stem, cases in stems:
        for case in cases:
            derived = list(stemmer([case]))[0]
            if derived != stem:
                errors.append(case + ' -> ' + derived + ' instead of ' + stem)
    if errors:
        print("\n".join(errors))
        test.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
