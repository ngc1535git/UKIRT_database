# insertImage.py
#
# Insert an image reference and metadata into the database
#

from parseImageMetaData import parseImageMetaData

import re

# Insert a single image reference and metadata into the DB
# Args: database cursor, string, astropy FITS header (dict)
# Returns: int
def insertImage(dbCursor, imageFileName, imageHeader):

	#Parse info from the image header
	imageData = parseImageMetaData(imageHeader)

	#Add image to db if doesn't exist
	sql = "INSERT OR IGNORE INTO images (imageFile, msb_title, telescope, instrument, target, type, start_time, end_time, exposure, filter, sensor_temp, air_temp, gain, n_reads, read_mode, focus, tel_ra, tel_dec, ra_rate, dec_rate, airmass, darkFile, flatFile, reduced, astrometry, pp_aperture) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
	imageData.insert(0, imageFileName)
	dbCursor.execute(sql, imageData)
	imageAdded = dbCursor.rowcount

	#Add satellite to db if doesn't exist
	satAdded = 0
	msbRegex = re.search(r"^\d+", imageData[1])
	if msbRegex is not None:
		satID = msbRegex.group()
		sql = "INSERT OR IGNORE INTO sats (norad_id) VALUES (?);"
		dbCursor.execute(sql, [satID])
		satAdded = dbCursor.rowcount

	return (imageAdded, satAdded)




# from astropy.io import fits

# # Open a FITS file and extract data
# # Args: filename = string
# # Return: metadata dictionary, image data array
# def openFITS(filename):
# 	hdul = fits.open(filename)
# 	header = hdul[0].header
# 	data = hdul[0].data
# 	hdul.close()
# 	return header, data



# file = 'y20210203_00672_r_a.fits'

# header, data = openFITS(file)

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

# temp = insertImage(cursor, file, header)

# print(temp)

# conn.commit()