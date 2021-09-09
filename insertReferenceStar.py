# insertReferenceStar.py
#
# Insert the zeropoint magnitude and stuff for reference stars from each sidereal image
#


# Insert a single reference star magnitude and metadata into the DB
# Args: database cursor, list of things
# Returns: int
def insertReferenceStar(dbCursor, data):

	#Add image to db if doesn't exist
	sql = "INSERT OR IGNORE INTO referenceStars (image_id, photometric_catalog, ra, decl, alt, az, airmass, inst_mag, inst_mag_error, magnitude, magnitude_error, zeropoint, zeropoint_error, fwhm, sextractor, rejected) VALUES ((SELECT id FROM images WHERE imageFile = ?), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
	dbCursor.execute(sql, data)
	refStarAdded = dbCursor.rowcount

	return refStarAdded


