#
# Reads a test case file and generates the commands to the virtualdriver
#
from util import parsedoubles
from util import base_splitstring
import ntpath

class TestCaseReader:
	def __init__(self, filename):
		self.filename = filename
		self.error = ""
		self.data = []
		self.currentButtonState = 0
		try:
			f = open(filename, "r")
		except:
			return
		contents = f.readlines()
		f.close()
		for i in range(0, len(contents)):
			s = contents[i]
			s = s[0:len(s)-1]
			if (len(s)==0):
				return
			res = base_splitstring(s,"\t")
			print (65, res)
			if not self.makeCommand(i+1, res):
				return

	def tellfilename(self):
		head, tail = ntpath.split(self.filename)
		return tail

	def size(self):
		return len(self.data)

	def makeerror(self, lineno, col, msg):
		self.error = "line:" + str(lineno) + " column:" + str(col) + " " + msg
		return False

	def validAxis(self, c):
		if (c == 'G' or c == 'g'):
			return True
		if (c == 'S' or c == 's'):
			return True
		if (c == 'D' or c == 'd'):
			return True
		if (c == 'F' or c == 'f'):
			return True
		return False

	def makeCommand(self, lineno, tokens):
		if len(tokens) < 2:
			return self.makeerror(lineno, 1, " Too short line")

		# get time
		try:
			t = (float)(tokens[0]);
		except:
			return self.makeerror(lineno, 1, "Invalid time")
		# check if buttons are given
		firstcolumn = 0
		emptycolumntwo = 0
		try:
			v = (float)(tokens[1])
			firstcolumn = 1
			emptycolumntwo = 1
		except:
			# not a number, see if it is a valid cmd
			token = tokens[1]
			for i in range(0, len(token)):
				if (not self.validAxis(token[i])):
					return self.makeerror(lineno, 2, "Invalid value")
			# valid key combination
			self.makeKeyCommand(t, token)
			firstcolumn = 2
		# See if more columns
		if (len(tokens) == firstcolumn):
			return True # no pos or rot
		# check that all columns are numbers
		for i in range(firstcolumn, len(tokens)):
			try:
				v = (float)(tokens[i])
			except:
				return self.makeerror(lineno, i+emptycolumntwo+1, "Invalid number")
		self.makePosCommand(t, firstcolumn, tokens)
			
		return True

	def makeKeyCommand(self, time, token):
		self.setCurrentButtonState(token)
		self.data.append("k " + str(time) + " " + str(self.currentButtonState))

	def makePosCommand(self, time, firstcolumn, tokens):
		s = ""
		for i in range(firstcolumn, len(tokens)):
			s = s + tokens[i] + " "
		self.data.append("s " + str(time) + " " + s)

	def setCurrentButtonState(self, token):
		for i in range(0,len(token)):
			if (token[i] == 'S'):
				self.currentButtonState = self.currentButtonState|0x1
			elif (token[i] == 's'):
				self.currentButtonState = self.currentButtonState&0xE
			elif (token[i] == 'D'):
				self.currentButtonState = self.currentButtonState|0x2
			elif (token[i] == 'd'):
				self.currentButtonState = self.currentButtonState&0xD
			elif (token[i] == 'F'):
				self.currentButtonState = self.currentButtonState|0x4
			elif (token[i] == 'f'):
				self.currentButtonState = self.currentButtonState&0xB
			elif (token[i] == 'G'):
				self.currentButtonState = self.currentButtonState|0x8
			elif (token[i] == 'g'):
				self.currentButtonState = self.currentButtonState&0x7

