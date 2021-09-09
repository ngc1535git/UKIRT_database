# rejectTarget.py
#
# Update target measurements which have been rejected
#


# Update target entry in database with rejection flag
# Args: database cursor, imageFile string
# Returns: int
def rejectTarget(dbCursor, imageFile):

	#Update rejection flag
	sql = "UPDATE targets SET rejected = True WHERE image_id = (SELECT id FROM images WHERE imageFile = ?);"
	dbCursor.execute(sql, [imageFile])
	targetRejected = dbCursor.rowcount

	return targetRejected

