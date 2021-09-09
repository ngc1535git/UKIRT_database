# postProcessDB.py
#
# Query the database for info and compute new info 
#
# Call from command python3 postprocessDB.py <databaseFile>
# -e to compute satellite ephemeris
#



import argparse
import os
import sqlite3
import numpy as np
from skyfield import api

from locations import *
from satFunctions import *
from pickeringAirmass import pickeringAirmass

location = locations["UKIRT"]


#######################################################################################################################

# Make a clean new log file
# Args: nothing
# Returns: nothing
def createLog():
	f = open("errorLog.txt", "w")
	f.write("")
	f.close()


# Write a list of files which weren't succesful
# Args: badFile = string, error = string
# Returns: nothing
def appendLog(badFile, error):
	f = open("errorLog.txt", "a")
	f.write(badFile + " - " + error + "\n")
	f.close()


# Retrieve best match TLE from a database
# Args: dbCursor = db cursor object, satList = array of num, data = datetime object, maxAge = num, source = string
# Returns: array of string
def loadTLEsFromDatabase(dbCursor, satList, date, maxAge=48, source="Celestrak_Supplemental"):

	tleList = []

	minDate = date - dt.timedelta(hours=maxAge)
	maxDate = date + dt.timedelta(hours=maxAge)


	#Download latest TLE for each satellite
	try:
		print("Downloading TLE data...")

		for s in satList:
			try: 
				dbCursor.execute( "SELECT tle FROM tles WHERE norad_id = ? AND source = ? AND epoch > ? AND epoch < ? ORDER BY epoch DESC", [s, source, minDate.strftime('%Y-%m-%d %H:%M:%S'), maxDate.strftime('%Y-%m-%d %H:%M:%S')] )

				temp = [s[0] for s in dbCursor]

				if len(temp) == 0:
					print("... no TLE found for", s)
				else:
					tleList += [temp[0].splitlines()]
			except Exception as e:
				print("\tCould not load TLE for", s)
				print(e)

	except Exception as e:
		print("Could not retrieve TLE data!")
		print(e)


	return tleList


# Fetch the internal database ID of a TLE
# Args: dbCursor = db cursor object, tle = string
# Returns tle id
def fetchTLEID(dbCursor, tle):

	#Query db for sat id
	print("Querying database for ID# of TLE...")
	try:
		dbCursor.execute( "SELECT id FROM tles WHERE tle = ?", [tle] )
		output = [s[0] for s in dbCursor]

		if len(output) == 0:
			print("No entry for tle")
			return None

		else:
			return output[0]

	except Exception as e:
		print("Failed!")
		print(e)

	return None






# Main function to query database and compute thigs
# Args: dbCursor = sqlite cursor, <flags to add things or not>
# Returns: nothing
def postProcessDB(dbCursor, addEphemeris=False, addMagnitudes=False):

	if addEphemeris:
		print("\n################################################################################\n")
		print("Querying database for list of targets...")

		#Query databse for target ids and observation time
		sql = "SELECT targets.id, sats.norad_id, images.start_time, images.exposure, targets.ra, targets.decl FROM ((sats INNER JOIN targets ON sats.id = targets.target_id) INNER JOIN images ON targets.image_id = images.id) WHERE tle_id IS NULL;"
		targetObservations = list(dbCursor.execute(sql))

		#Iterate through targets
		for row in targetObservations:

			targetID = row[0]
			satID = row[1]

			midExpTime = dt.datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S.%f") + dt.timedelta(seconds=row[3]/2)
			maxTLEAge = 24*365
			tleSource = "Spacetrack"
			telRA = row[4]
			telDec = row[5]

			# Query db for TLE
			tle = loadTLEsFromDatabase(dbCursor, [satID], midExpTime, maxTLEAge, tleSource)

			if tle == []:
				print("Failed to find TLE!")
				continue
			else:
				tle = tle[0]

			# Get TLE id
			tleID = fetchTLEID(cursor, '\n'.join([str(x) for x in tle]))

			if tleID == None:
				print("Failed to find TLE ID!")
				continue

			# Determine tle age
			tleAge = midExpTime - parseTLEdate(tle)

			# print(tleAge)

			# Compute ephemeris
			ephemeris = computeEphemeris(tle, location, midExpTime.replace(tzinfo=api.utc))

			# print(ephemeris)

			# Check target pointing errors
			ra_error = telRA - ephemeris['ra']#*360/24
			dec_error = telDec - ephemeris['dec']

			separation = np.degrees(elongation(np.radians(telRA), np.radians(telDec), np.radians(ephemeris['ra']), np.radians(ephemeris['dec'])))

			# print(ra_error)
			# print(dec_error)
			# print(separation)

			# Build package for db insert
			result = {
					"tle_id" : tleID,
					"tle_age" : tleAge.total_seconds(),
					"ra_predicted" : ephemeris['ra'],#*360/24,
					"decl_predicted" : ephemeris['dec'],
					"ra_error" : ra_error,
					"decl_error" : dec_error,
					"pointing_error" : separation,
					"ra_rate_predicted" : ephemeris['raRate'],
					"dec_rate_predicted" : ephemeris['decRate'],
					"velocity_predicted" : ephemeris['velocity'],
					"alt_predicetd" : ephemeris['altitude'],
					"az_predicted" : ephemeris['azimuth'],
					"lat_predicted" : ephemeris['lat'],
					"lon_predicted" : ephemeris['lon'],
					"airmass_predicted" : pickeringAirmass(ephemeris['altitude']),
					"orbit_height_predicted" : ephemeris['height'],
					"range_predicted" : ephemeris['range'],
					"sun_elong_predicted" : ephemeris['sunElong'],
					"eclipsed" : ephemeris['eclipsed'],
					"target_id" : targetID
				}

			# print(result)

			#Update entry in db
			sql = "UPDATE targets SET tle_id = ?, tle_age = ?, ra_predicted = ?, decl_predicted = ?, ra_error = ?, decl_error = ?, pointing_error = ?, ra_rate_predicted = ?, decl_rate_predicted = ?, velocity_predicted = ?, alt_predicted = ?, az_predicted = ?, lat_predicted = ?, lon_predicted = ?, airmass_predicted = ?, orbit_height_predicted = ?, range_predicted = ?, sun_elong_predicted = ?, eclipsed = ? WHERE id = ?;"
			dbCursor.execute(sql, list(result.values()))
			targetUpdated = dbCursor.rowcount

			print("Added", targetUpdated, "results!")










#######################################################################################################################

parser = argparse.ArgumentParser()
parser.add_argument("databaseFile", help="path to database file")
parser.add_argument("-e", "--ephemeris", help="compute target ephemeris from TLE", action="store_true")



args = parser.parse_args()

createLog()
databaseFile = os.fsencode(args.databaseFile)
addEphemeris = args.ephemeris



# cwd = os.getcwd()
# directory = os.path.join(os.fsencode(cwd), os.fsencode("temp"))
# overwrite = True


# Open database file (will create new one if not exist)
try:
	print("Opening database...")
	conn = sqlite3.connect(databaseFile)
except Exception as e:
	print("Failed!")
	print(e)
	exit()

print("Success!")

cursor = conn.cursor()

#Add things to database
postProcessDB(cursor, addEphemeris)

#Commit changes to database
conn.commit()
conn.close()