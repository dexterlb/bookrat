import regex
import json
from collections import defaultdict
import time

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
			counted_words[word] += 1
		return dict(counted_words)

	def count_stemmed_words(self, book):
		started = time.time()
		stemmed = list(self.stemmer(self.split_text(book.text)))
		print("stemmed in: " + str(time.time()-started))
		return self.count_words(stemmed)