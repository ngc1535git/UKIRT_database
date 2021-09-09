# computeAltAz.py
#
# Compute the altitude and azimuth from a RA and Dec
#


import skyfield.api
from locations import *

# Compute the alt az from an RA and Dec
# Args: juliandate = num, location = string, ra = num, dec = num
# Returns: two nums
def computeAltAz(juliandate, location, ra, dec):

	#Load stuff
	planets = skyfield.api.load('de421.bsp')
	ts = skyfield.api.load.timescale()
	earth = planets['earth']

	#Load location info
	loc = locations[location]

	# Use RA and Dec to make Star object
	coords = skyfield.api.Star(ra=skyfield.api.Angle(degrees=ra), dec_degrees=dec)

	#Time
	time = ts.tt_jd(juliandate)

	#Compute things
	l = (earth + loc).at(time)
	o = l.observe(coords).apparent()
	alt = o.altaz()[0]
	az = o.altaz()[1]

	return alt.degrees, az.degrees


#Test

# alt, az = computeAltAz(2459327.4718, "Bigelow", (7+45/60+18.9/3600)/24*360, 28+1/60+35.0/3600)
# print(alt, az)


