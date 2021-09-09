# satFunctions.py
#
# Functions for computing satellite related things with Skyfield
#
# Harry Krantz
# Steward Observatory
# University of Arizona
# Copyright May 2020
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import datetime as dt
import numpy as np

import skyfield.api


# Compute the ephemeris and other parameters for a given TLE, location, and singular time
# Args: tle = string, loc = skyfield topos, time = Skyfield Time or datetime
# Returns: dict
def computeEphemeris(tle, loc, time):

	#Split the tle
	name, line1, line2 = tle
	noradID = parseTLEID(tle)


	#Initialization of things
	sat = skyfield.sgp4lib.EarthSatellite(line1, line2, name)
	ts = skyfield.api.load.timescale()
	
	planets = skyfield.api.load('de421.bsp')
	earth = planets['earth']
	moon = planets['moon']
	sun = planets['sun']


	#Convert time if needed
	if type(time) == dt.datetime:
		time = ts.utc(time)


	#Compute satellite position
	geocentric = sat.at(time)
	subpoint = geocentric.subpoint()
	lat = subpoint.latitude
	lon = subpoint.longitude
	ele = subpoint.elevation

	difference = sat - loc
	topocentric = difference.at(time)
	alt, az, distance = topocentric.altaz()
	ra, dec, temp = topocentric.radec()


	#Angular velocity per second
	#Step time forward one second and get the difference in pointing	
	velocity = topocentric.separation_from( difference.at(ts.tt_jd(time.tt + 1/86400)) )

	newTopocentric = difference.at(ts.tt_jd(time.tt + 1/86400))
	newRa, newDec, temp = newTopocentric.radec()

	raRate = newRa._degrees - ra._degrees
	decRate = newDec.degrees - dec.degrees

	
	#Skyfield does not have a built-in eclipsed function like PyEphem does :(
	#This is a crude way of doing it but should be fine for this purpose
	geocentricElong = geocentric.separation_from( earth.at(time).observe(sun) )
	geocentricDist = geocentric.distance()
	sunVectorSep = np.cos(geocentricElong.radians - np.pi/2) * geocentricDist.km
	earthRadius = 6378 #km
	umbraWidth = earthRadius - max(0, np.tan(np.radians(0.25)) * (np.sin(geocentricElong.radians - np.pi/2) * geocentricDist.km))
	eclipsed = sunVectorSep < umbraWidth
	

	#Determine if sun or moon is up and corresponging elongations
	l = (earth + loc).at(time)
	m = l.observe(moon).apparent()
	s = l.observe(sun).apparent()

	mAlt = m.altaz()[0]
	sAlt = s.altaz()[0]

	sunUp = sAlt.degrees > 0
	sunElong = topocentric.separation_from(s)

	moonUp = mAlt.degrees > 0
	moonElong = topocentric.separation_from(m)


	#Format output into dictionary
	passs = {
				"name" : name.strip(),
				"id" : noradID,
				"time" : time.utc_datetime(),
				"range" : distance.km,
				"height" : ele.km,
				"altitude" : alt.degrees,
				"azimuth" : az.degrees,
				"ra" : ra._degrees,
				"dec" : dec.degrees,
				"raRate" : raRate,
				"decRate" : decRate,
				"lat" : lat.degrees,
				"lon" : lon.degrees,
				"velocity" : velocity.degrees,
				"sunElong" : sunElong.degrees,
				"moonElong" : moonElong.degrees,
				"eclipsed" : eclipsed,
				"sunUp" : sunUp,
				"moonUp" : moonUp
			}

	return passs




# def printEphemeris(ephemeris):
# 	print("{: <24} {: <8} {: <21} {: <14.7s} {: <21} {: <10.7s} {: <14.7s} {: <21} {: <13.7s} {: <13.7s}".format(*map(str, [ephemeris["name"], ephemeris["id"], ephemeris["time"].strftime('%Y-%m-%d %H:%M:%S'), ephemeris["azimuth"], ephemeris["altitude"], ephemeris["ra"], ephemeris["dec"], ephemeris["lat"], ephemeris["lon"], ephemeris["velocity"], ephemeris["range"], ephemeris["height"], ephemeris["ra"] ],)))



# def printPassList(passes):
# 	#Print the header and list of passes
# 	headers = ["Name", "ID", "Rise Time", "Rise Azimuth", "Peak Time", "Peak Alt", "Peak Azimuth", "Set Time", "Set Azimuth", "Duration"]
# 	print("{: <24} {: <8} {: <21} {: <14} {: <21} {: <10} {: <14} {: <21} {: <13} {: <13}".format(*headers))
# 	print("----------------------------------------------------------------------------------------------------------------------------------------------------------------------")
# 	for p in passes:
# 		printPass(p)




# Extract the epoch date from a TLE
# Args: tle = array of string
# Return: datetime 
def parseTLEdate(tle):
	year = int("20" + tle[1][18:20])
	day = float(tle[1][20:33])

	return dt.datetime(year-1,12,31,0,0,0) + dt.timedelta(day)




# Extract the NORAD ID from a TLE
# Args: tle = array pf string
# Returns: string
def parseTLEID(tle):
	return tle[1][2:8]




# Split TLE into the two/three lines
# Args: tle = array of string
# Returns: three strings
def splitTLE(tle):
	#Split on newline characters
	lines = tle.split("\n")

	#Actual TLE data should always be the last two lines
	line1 = lines[-2]
	line2 = lines[-1]

	#Check if there are three lines
	if len(lines) > 2:
		name = lines[0]
	else:
		name = "NONAME"

	return name, line1, line2




# Print the lines of a TLE
# Args: tle = array of string
# Returns: nothing
def printTLE(tle):
	for line in tle:
		print(line)




# Compute the checksum for a single TLE line
# Args: line = string
# Returns: num
def checksum(line):
	sum = 0
	for ch in line[:-1]:
		if ch.isdigit():
			sum += int(ch)
		if ch == "-":
			sum += 1
	return sum%10




# Compute and replace the checksum for a single TLE line
# Args: line = string
# Returns: string
def fixChecksum(line):
	return line[:-1] + str(checksum(line))



#Compute the elongation between two (ra,dec), must be in radians
def elongation(ra1, dec1, ra2, dec2):
	return np.arccos(np.sin(dec1)*np.sin(dec2) + np.cos(dec1)*np.cos(dec2)*np.cos(ra1 - ra2))



#  53.46721664899972 |  50.147600526245235 |  118.3210811540933 | -48.177141875391875

# temp = np.degrees(elongation(53.46721664899972,50.147600526245235,118.3210811540933,-48.177141875391875))

# print(temp)

