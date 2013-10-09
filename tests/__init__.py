from nose.tools import *
import codecs
from highlighter import *

def setup():
	pass

def teardown():
	pass

def test_parser():
	f = codecs.open('texts/yahoo_news', encoding='utf-8')
	texts= f.read()
	
	#print texts[89:108].encode('utf-8')
	# just care about the length
	# Highlighter( legthOfText )
	highlighter= Highlighter(len(texts))

	#list of the highlights, use generator for tests
	def notes():
		for index in range(20):
			yield [89, 108]

	# parse the notes
	lists= highlighter.parse(notes())
	for highlight in lists:
		print texts[highlight['up']:highlight['down']].encode('utf-8')

	