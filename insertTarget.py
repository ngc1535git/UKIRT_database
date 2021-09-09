# insertTarget.py
#
# Insert the target magnitude and stuff from each target image
#


# Insert a single target magnitude and metadata into the DB
# Args: database cursor, list of things
# Returns: int
def insertTarget(dbCursor, data):

	#Add image to db if doesn't exist
	sql = "INSERT OR IGNORE INTO targets (image_id, target_id, ra, decl, inst_mag, inst_mag_error, fwhm, sextractor) VALUES ((SELECT id FROM images WHERE imageFile = ?), (SELECT id FROM sats WHERE norad_id = (SELECT target FROM images WHERE imageFile = ?)), ?, ?, ?, ?, ?, ?);"
	dbCursor.execute(sql, data)
	targetAdded = dbCursor.rowcount

	return targetAdded

