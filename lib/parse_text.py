import regex
import json
from collections import defaultdict

class TextParser:
	def __init__(self, stemmer):
		self.word_splitter = regex.compile(r'\b\p{Ll}+\b')
		self.stemmer = stemmer

	def split_text(self, text):
		for word in self.word_splitter.findall(text):
			yield word.lower()

	def count_words(self, words):
		print("counting stemmed words")
		counted_words = defaultdict(int)
		for word in words:
			print("counting")
			counted_words[word] += 1
		return dict(counted_words)

	def count_stemmed_words(self, book):

		words_in_book = list(self.split_text(book.text))
		with open("foo.txt", "w") as f:
			json.dump(words_in_book, f)
		print("prepare to stem")
		stemmed = list(self.stemmer(words_in_book))
		print("stemmed!")
		return self.count_words(stemmed)