from big_string import *

class Highlighter(object):
	"""ldar Highlighter
	input: list of word highlights
	output: where the highlights are
	"""

	def __init__(self, length):
		self.textLength= length

	def parse(self, textList):
		parser= Parser()
		return parser.parse(textList, self.textLength)

