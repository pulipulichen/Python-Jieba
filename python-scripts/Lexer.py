"""
 * pyPOS
 *
 * Python Version Copyright 2011 Thomas Winningham
 * Javascript Version and Comments Copyright 2010, Percy Wegmann
 * Licensed under the GNU LGPLv3 license
 * http://www.opensource.org/licenses/lgpl-3.0.html

Part of Speech Lexer

"""
import re

# Used in fillArray
LEVEL_ONE  = re.compile('[^ \t\n\r]+'		,re.IGNORECASE)
LEVEL_TWO  = re.compile('[^ \t\n\r]+')

# Split by numbers, then whitespace, then punctuation
REGEXES    = [
		re.compile("[0-9]*\.[0-9]+|[0-9]+"	,re.IGNORECASE), 
		re.compile("[ \t\n\r]+"		,re.IGNORECASE), 
		re.compile("[\.\,\?\!]"		,re.IGNORECASE)
]

class LexerNode:
	def __init__(self, string, regex, regexs):
		self.string = string
		self.children = []
		childElements = None
		if string:
			self.matches =  regex.findall(string)
			childElements = regex.split(string)
		if 'matches' not in dir(self):
			self.matches = []
			childElements = [string]
		if len(regexs) > 0:
			nextRegex = regexs[0]
			nextRegexes = regexs[1:]
			for x in childElements:
				self.children.append(LexerNode(x, nextRegex, nextRegexes))
		else:
			self.children = childElements
	def fillArray(self,arr):
		global LEVEL_ONE, LEVEL_TWO
		for x in range(len(self.children)):
			child=self.children[x]
			if "fillArray" in dir(child):
				child.fillArray(arr)
			elif LEVEL_ONE.findall(child):
				arr.append(child)
			if (x < len(self.matches)):
				match = self.matches[x]
				if LEVEL_TWO.findall(match):
					arr.append(match)

class Lexer:
	def __init__(self):
		global REGEXES
    		self.regexs = REGEXES
	def lex(self,string):
		arr = []
		node = LexerNode(string,self.regexs[0],self.regexs[1:])
		node.fillArray(arr)
		return arr


if __name__ == "__main__":
	lexer = Lexer()
	print repr(lexer.lex("I made $5.60 today in 1 hour of work.  The E.M.T.'s were on time, but only barely."))

