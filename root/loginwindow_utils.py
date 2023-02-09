 ################################

import os
import random

DEBUG_FILE_NAME = "debug.txt"
PATH_TO_SAVE_DATA = "pack/"
NAME_OF_DATA_FILE = PATH_TO_SAVE_DATA+"saved_"

			
def writeFile(filename,str):
	try:
		f = open(filename , "a")
		f.write(str)
		f.close()
		return True
	except:
		try:
			f = open(filename , "w")
			f.write(str)
			f.close()
			return True
		except:
			return False
			
def existFile(str):
	try:
		file = open(str , "r")
		file.close()
		return True
	except:
		return False
		
		
		
def debugLine(str):
	if existFile(DEBUG_FILE_NAME):
		try:
			dbg_file = open(DEBUG_FILE_NAME , "a")
			dbg_file.write(str+"\n")
			dbg_file.close()
			return True
		except:
			return False
	else:
		try:
			dbg_file = open(DEBUG_FILE_NAME , "w")
			dbg_file.write(str+"\n")
			dbg_file.close()
			return True
		except:
			return False
		
def deleteFile(str):
	try:
		os.remove(str)
		return True
	except:
		return False
		
def resetFile(str):
	try:
		fr = open(str , "w")
		fr.close()
		return True
	except:
		return False
		
		
def getLinesFromFile(str):
	try:
		fr = open(str,"r")
		lines = fr.readlines()
		fr.close()
		return lines
	except:
		return []
		
def initDataFile():
	for i in xrange(0,4):
		name_of_file = NAME_OF_DATA_FILE+str(i)
		if not existFile(name_of_file):
			resetFile(name_of_file)


#crypt and decrypt func sample begin 		
def checkInvalidChar(first_number,second_number):
	first_is_invalid = False
	second_is_invalid = False
	if first_number == ord("#") or first_number == ord("^"):
		first_is_invalid = True
	if first_number < 32 or first_number == 127 or first_number > 254:
		first_is_invalid = True
	if second_number == ord("#") or second_number == ord("^"):
		second_is_invalid = True
	if second_number < 32 or second_number == 127 or second_number > 254:
		second_is_invalid = True
	if first_is_invalid or second_is_invalid:
		return True
	return False

def getNumberCoefficient(number):
	new_first = random.randint(1,150)
	new_second = number - new_first
	return new_first,new_second
	
def cryptChar(char):
	number = ord(char)
	number = (number + 20)*2 #now the number is pair
	rand_number = random.randint(1,100)
	if rand_number > 75:
		number+=55
		char_delimitation = "#"
	elif rand_number > 45:
		number+=12
		char_delimitation = "^"
	else:	
		number+=17
		char_delimitation = "&"
	split_number = 0
	split_number2 = 0	
	while checkInvalidChar( split_number , split_number2):
		split_number , split_number2 = getNumberCoefficient(number)
	
	
	return char_delimitation+chr(split_number)+chr(split_number2)
	
def decryptChar(arg , string):
	sum_result = 0
	for char in string:
		sum_result+= ord(char)
	if arg == "#":
		sum_result-=55
	elif arg == "^":	
		sum_result-=12
	elif arg == "&":
		sum_result-= 17
	sum_result = sum_result/2
	sum_result-=20	
	return chr(sum_result)
	
def cryptString(string):
	crypted_string = ""
	for char in string:
		crypted_string+=cryptChar(char)
	return crypted_string
	
def decryptString(string):
	length = len(string)
	
	decripted_string = ""
	
	idx = 0
	while idx < length:
		if string[idx] == "#" or string[idx] == "^" or string[idx] == "&" :
			try:
				decripted_string+=decryptChar(string[idx],string[idx+1:idx+3])
			except:
				pass
			idx+=3
	return decripted_string
			
	
#end of crypt and decrypt func



class saveLoginDataFile():
	
	def __init__(self,index):
		self.index = index
		self.name = NAME_OF_DATA_FILE+str(index)
		
		self.is_already_written = False
		
		self.loadLoginDataFromFile()
		
	def loadLoginDataFromFile(self):
		if existFile(self.name):
			self.lines = getLinesFromFile(self.name)
			
			if len(self.lines) == 0:
				self.is_already_written = False
				return
				
			split_data = self.lines[0].split("\t")
			if len(split_data) != 2:
				resetFile(self.name)
				self.is_already_written = False
				return
			
			self.id = split_data[0]
			self.password = decryptString(split_data[1])
			self.is_already_written = True		
			return
		
		resetFile(self.name)
		
	
	def isEmptyDataFile(self):
		return not self.is_already_written
	
	def writeDataInFile(self, id , password):
		if not self.isEmptyDataFile():
			return False
			
		if writeFile(self.name , "%s\t%s"%(id ,cryptString(password))):
			self.is_already_written = True
			return True
			
		resetFile(self.name)
		return False
	
	def getID(self):
		if not self.isEmptyDataFile():
			return self.id
		return ""
		
	def getPassword(self):
		if not self.isEmptyDataFile():
			return self.password
		return ""
		
	
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		