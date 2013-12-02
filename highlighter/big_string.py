from itertools import izip

def pairwise(iterable):
    "s -> (s0,s1), (s2,s3), (s4, s5), ..."
    a = iter(iterable)
    return izip(a, a)

# get the list
# do the word counts
# find min sup board
# get the max counts in the interval

class Parser(object):
	"""algorithm of lidar popular highlights"""

	def __init__(self):
		self.lookFor= 'up' # the gap we lookin for while iteration
		# min sup
		self.minSup= 30
		# list conctains all intervals
		self.blocks= []
		# list return
		self.hlts= []

	def checkSup(self, char):
		if self.lookFor == 'up':
			return char >= self.minSup
		else: # down
			return char < self.minSup

	def changeTarget(self):
		if self.lookFor == 'up':
			self.lookFor= 'down'
		else:
			self.lookFor= 'up'

	def found(self, idx):
		self.blocks.append(idx)
		self.changeTarget()

	def parse(self, lists, length):
		# init the texts list, start from zero
		texts= [0]*length

		# add the count
		# iterate notes [ [0,1], [2,1] ... ]
		for note in lists:
			# get the interval of note
			# range(note[0], note[1])= [1,2,3...14]
			for x in range(note[0], note[1]):
				texts[x]= texts[x]+1

		# find min sup
		# start from zero
		# if larger then min sup
		# save it in a list, and move next
		# but lookin for smaller than min sup
		# find the boarders, save it to list
		# start from the gap, iterate
		for idx, char in enumerate(texts):
			if self.checkSup(char):
				self.found(idx)

		# count the max in blocks
		for up, down in pairwise(self.blocks):
			maxSup= max(texts[up:down])
			dicts= { 'up': up, 'down': down, 'counts': maxSup }
			self.hlts.append(dicts)

		# return the hlts
		return self.hlts




