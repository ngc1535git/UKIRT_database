# insertTLE.py
#
# Insert a parsed TLE into the database table
#

from parseTLE import parseTLE


# Insert a single TLE into the DB
# Args: database cursor, array of string
# Returns: list of int
def insertTLE(dbCursor, tle, source):

	#Parse the TLE
	tleData = parseTLE(tle)

	#Put the TLE together for record keeping
	tleData.insert(0, "\n".join(tle))

	#Add sat to db if doesn't exist
	sql = "INSERT OR IGNORE INTO sats (name, norad_id, international_id, deorbited) VALUES (?, ?, ?, ?);"
	dbCursor.execute(sql, [tleData[1], tleData[2], tleData[4], 0])
	satAdded = dbCursor.rowcount

	#Update sat in db if does exist
	sql = "UPDATE sats SET name = ?, international_id = ?, deorbited = ? WHERE norad_id = ?;"
	dbCursor.execute(sql, [tleData[1], tleData[4], 0, tleData[2]])
	satUpdated = dbCursor.rowcount

	#Add TLE to db if doesn't exist
	sql = "INSERT OR IGNORE INTO tles (sat_id, tle, sat_name, norad_id, classification, international_id, epoch_year, epoch_day, first_deriv_mm, second_deriv_mm, drag, type, element_num, inclination, ra_node, eccentricity, arg_perigee, mean_anomaly, mean_motion, revolution_num, epoch, source) VALUES ((SELECT id FROM sats WHERE norad_id = ?), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
	tleData.insert(0, tleData[2])
	tleData.append(source)
	dbCursor.execute(sql, tleData)
	tleAdded = dbCursor.rowcount

	return [satAdded, satUpdated, tleAdded]





# test = ["STARLINK-31             ",
# 		"1 44235C 19029A   20212.69624933  .00941183  00000-0  72658-2 0  2122",
# 		"2 44235  52.9915   0.1578 0001305  75.9665   0.7419 15.70322315    10"
# 		]

# import sqlite3
# databaseFileName = "test.db"

# # Open database file (will create new one if not exist)
# try:
# 	print("Opening database...")
# 	conn = sqlite3.connect(databaseFileName)
# except Exception as e:
# 	print("Failed!")
# 	print(e)
# 	exit()

# print("Success!")

# cursor = conn.cursor()

# insertTLE(cursor, test, "local")

# conn.commit()




