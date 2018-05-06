"""
 * pyPOS
 * 
 * Python Version Copyright 2011 Thomas Winningham
 * Javascript Version and Comments Copyright 2010, Percy Wegmann
 * Licensed under the LGPLv3 license
 * http://www.opensource.org/licenses/lgpl-3.0.html

Parts of Speech Tagger

"""

from Lexicon import POSTAGGER_LEXICON

def is_number(s):
	'''Simple test of string for number'''
	try:
		float(s)
		return True
	except ValueError:
		return False


class POSTagger:
	def __init__(self):
		global POSTAGGER_LEXICON
		self.lexicon = POSTAGGER_LEXICON
	def wordInLexicon(self,word):
		'''Test if the word exists in the lexicon'''
		if self.lexicon.has_key(word):
			return True
		# 1/22/2002 mod (from Lisp code): if not in hash, try lower case:
		else:
			if self.lexicon.has_key(word.lower()):
				return True
		return False
	def tag(self,words):
		'''Tag a list of words'''
		ret=[None for x in range(len(words))]
		for x in range(len(words)):
			ss = False
			word = words[x]
			if self.lexicon.has_key(word):
				ss = self.lexicon[word]
			# 1/22/2002 mod (from Lisp code): if not in hash, try lower case:
			if not ss:
				word = word.lower()
				if self.lexicon.has_key(word):
					ss = self.lexicon[word]
			if (not ss and len(word) == 1):
				ret[x] = words[x] + "^"
			if not ss:
				ret[x] = "NN"
			else:
				ret[x] = ss[0]
		#Apply transformational rules
		for x in range(len(words)):
			word=ret[x]
			#  rule 1: DT, {VBD | VBP} --> DT, NN
			if x > 0 and ret[x-1] == "DT":
				if word == "VBD" or word == "VBP" or word == "VB":
					ret[x] = "NN"
			# rule 2: convert a noun to a number (CD) if "." appears in the word
			if word[0] == "N":
				if words[x].__contains__('.'):
					ret[x] = "CD"
				if is_number(words[x]):
					ret[x] = "CD"
			# rule 3: convert a noun to a past participle if words[i] ends with "ed"
			if ret[x][0] == "N" and words[x][-2:] == "ed":
				ret[x] = "VBN"
			# rule 4: convert any type to adverb if it ends in "ly";
			if ret[x][-2:] == 'ly':
				ret[x] = "RB"
			# rule 5: convert a common noun (NN or NNS) to a adjective if it ends with "al"
			if ret[x][:2] == "NN" and ret[x][-2:] == "al":
				ret[x] = ' '.join(str(x),"JJ")
			# rule 6: convert a noun to a verb if the preceding work is "would"
			if x > 0 and ret[x][:2] == "NN" and words[x-1].lower() == "would":
				ret[x] = "VB"
			# rule 7: if a word has been categorized as a common noun and it ends with "s",
			# then set its type to plural common noun (NNS)
			if ret[x] == "NN" and words[x][-1:] == "s":
				ret[x] = "NNS"
			# rule 8: convert a common noun to a present participle verb (i.e., a gerund)
			if ret[x] == "NN" and words[x][-3:] == "ing":
				ret[x] = "VBG"
		result = zip(words,ret)
		return result
		
if __name__ == "__main__":
	print POSTagger().tag(["i", "went", "to", "the", "store", "to", "buy", "5.2", "gallons", "of", "milk"])

