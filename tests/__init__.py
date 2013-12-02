from nose.tools import *
import codecs
from bs4 import BeautifulSoup
import requests, re
import psycopg2
from highlighter import *

def setup():
	pass

def teardown():
	pass

def test_parser():
	conn = psycopg2.connect("dbname=lidar user=william password=1234")
	cur = conn.cursor()

	url= 'http://www.parenting.com.tw/article/article.action?id=5050231'
	cur.execute('SELECT * FROM "Notes" WHERE uri=%s;', (url,))
	notes= cur.fetchall()
	# request
	r = requests.get(url)

	soup = BeautifulSoup(r.text)

	for tag in soup.find_all(True):
		if tag.name in ['script', 'noscript', 'iframe']:
			tag.extract()

	#def strContain(s):
	#	return (unicode(text,"utf-8") in unicode(s))

	#for tag in soup.findAll(text=True):
	#	print tag.strip().encode('utf-8')

	paragraph= soup.body.get_text(strip=True)
	# print paragraph.encode('utf-8')
	blocks= []
	for note in notes:
		text= unicode(note[1].strip(),"utf-8")
		textIdx= paragraph.find(text)
		if textIdx>=0:
			block= [textIdx, textIdx+len(text)]
			blocks.append(block)
		# print paragraph[textIdx:textIdx+len(text)].encode('utf-8')
		# -1 = not found
	#print blocks

	highlighter= Highlighter(len(paragraph))

	# parse the notes
	lists= highlighter.parse(blocks)
	for highlight in lists:
		highlightText= paragraph[highlight['up']:highlight['down']].encode('utf-8')
		highlightCount= highlight['counts']
		uni_highlightText= unicode(highlightText,"utf-8")
		# print highlightText, highlightCount
		def strContain(s):
			return (uni_highlightText in unicode(s))

		def constructPath(tag):
			# ['h3', 'div', 'div', 'div', 'div', 'body', 'html', u'[document]']
			i=1
			tagName= tag.name
			#print 'in ',tagName, len(tag), tag.attrs
			while tag.previousSibling:
				tag= tag.previousSibling
				if tag.name == tagName:
					#print tag.name, tag.attrs
					i += 1
			return (tagName, i)

		foundTag= soup.find(text= strContain)
		start= foundTag.find(uni_highlightText)
		end= start+len(uni_highlightText)
		tagPath= [constructPath(tag) for tag in foundTag.findParents()]
		xpath= ''
		while len(tagPath)>0:
			tag= tagPath.pop()
			if not tag[0]==u'[document]' and not tag[0]=='html' and not tag[0]=='body':
				tagName= tag[0]
				pos= tag[1]
				xpath += '/' + tagName + '[' + str(pos) + ']'
		print highlightCount
		print xpath,start,end