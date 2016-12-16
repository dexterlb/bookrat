import sys
from ..lib import parse_dictionary
from ..lib import megatron

def main():
	m = megatron.Megatron("postgres://do@localhost/book-rat-test")
	parser = parse_dictionary.DictionaryParser(m)
	json_file = sys.argv[1]
	parser.parse_dictionary_from(json_file)

if __name__ == '__main__':
	main()