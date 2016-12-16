import json
from . import database
from . import megatron

class DictionaryParser:
    def __init__(self, megatron):
        self.megatron = megatron

    def _parse_dictionary_from(self, json_dictionary):
        with open(json_dictionary) as data_file:    
            data = json.load(data_file)
            for subdictionary in data:
                type = subdictionary["type"]
                words = subdictionary["words"]
                for word in words:
                    yield database.Word(text=word, type=type, from_dictionary=True)

    def parse_dictionary_from(self, json_dictionary):
        self.megatron.word_controller.add_many(self._parse_dictionary_from(json_dictionary))