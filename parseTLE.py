# parseTLE.py
#
# Take a two or three line TLE and parse it into its elements


from datetime import datetime, timedelta


# Parse a single TLE
# Args: array of string
# Returns: array of TLE elements
def parseTLE(stringList):

	output = [None]*19

	#Line 0 aka title line
	if len(stringList) == 3:
		#Record the satellite name if provided
		output[0] = stringList[0].strip() #Satellite name

	#Line 1
	try:
		output[1] = int(stringList[-2][2:7]) #Satellite catalog number
		output[2] = stringList[-2][7].strip() #Classification
		output[3] = stringList[-2][9:17].strip() #International designator
		output[4] = int(stringList[-2][18:20]) #Epoch year
		output[5] = float(stringList[-2][20:32]) #Epoch day
		output[6] = float(stringList[-2][33:43]) #First derivative of mean motion
		output[7] = float(stringList[-2][44:50])*10**int(stringList[-2][50:52]) #Second derivative of mean motion
		output[8] = float(stringList[-2][53:59])*10**int(stringList[-2][59:61]) #Drag term
		output[9] = int(stringList[-2][62:63]) #Ephemeris type
		output[10] = int(stringList[-2][64:68]) #Element set number
	except Exception as e:
		print(e)
		return None

	#Line 2
	try:
		output[11] = float(stringList[-1][8:16]) #Inclination
		output[12] = float(stringList[-1][17:25]) #Right ascension of ascending node
		output[13] = float(stringList[-1][26:33]) #Eccentricity
		output[14] = float(stringList[-1][34:42]) #Argument of perigee
		output[15] = float(stringList[-1][43:51]) #Mean anomaly
		output[16] = float(stringList[-1][52:63]) #Mean motion
		output[17] = int(stringList[-1][63:68]) #Revolution number at epoch
	except Exception as e:
		print(e)
		return None

	#Make a handy timestamp for the epoch
	epoch = datetime(2000 + int(stringList[-2][18:20]) - 1, 12, 31) + timedelta(days=float(stringList[-2][20:32]))
	output[18] = epoch.strftime('%Y-%m-%d %H:%M:%S.%f')


	return output




# test = ["STARLINK-31             ",
# 		"1 44235C 19029A   20212.69624933  .00941183  00000-0  72658-2 0  2122",
# 		"2 44235  52.9915   0.1578 0001305  75.9665   0.7419 15.70322315    10"
# 		]

# print(parseTLE(test))




