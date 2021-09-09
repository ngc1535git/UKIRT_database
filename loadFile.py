# loadFile.py
#
# Various functions for loading TLEs from a file either locally or remote
# 


import requests




# Load TLE data from a local file
# Args: filename = path
# Returns: array 
def loadFile(filename):
	#OPen the file 
	f = open(filename)

	#load the lines into an array
	content = f.read().splitlines()

	output = parseTLEFile(content)

	return output


# Load TLE data from a local file
# Args: filename = path
# Returns: array 
def loadAdamTLEFile(filename):
	#OPen the file 
	f = open(filename)

	#load the lines into an array
	content = f.read().splitlines()

	output = parseAdamTLEFile(content)

	return output


# Load TLE data from a web hosted file
# Args: filename = path
# Returns: array
def loadFileURL(url):
	
	#Get stuff from the url
	f = requests.get(url)

	#load the lines into an array
	content = f.text.splitlines()

	if content[0] == 'No TLE found':
		return False

	output = parseTLEFile(content)

	return output


# Parse a loaded file of TLE data
# Args: array of string
# Returns: array
def parseTLEFile(stringList, satName="UNKOWN"):

	output = []

	#Separate each TLE set
	lineNum = 0
	while lineNum < len(stringList):
		#If first line
		if stringList[lineNum][0:2] == "1 ":
			output.append([satName] + stringList[lineNum:lineNum+2])
			lineNum += 2
		#If second line
		elif stringList[lineNum][0:2] == "2 ":
			lineNum += 1
		#Else assume title line
		else:
			output.append(stringList[lineNum:lineNum+3])
			lineNum += 3

	return output


# Parse a loaded file of TLE data
# Args: array of string
# Returns: array
def parseAdamTLEFile(stringList, satName="UNKNOWN"):

	output = []

	#Separate each TLE set
	lineNum = 0
	while lineNum < len(stringList):
		#If first line
		if stringList[lineNum][0:2] == "1 ":
			output.append([satName] + stringList[lineNum:lineNum+2])
			lineNum += 1
		#If second line
		elif stringList[lineNum][0:2] == "2 ":
			lineNum += 1
		#Else assume title line
		else:
			# output.append(stringList[lineNum:lineNum+3])
			lineNum += 1

	return output


# temp = loadAdamTLEFile("archived_TLE_catalog_new.txt")
# print(temp)


