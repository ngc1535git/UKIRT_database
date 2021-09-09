# parseImageMetaData.py
#
# Parse image meta data from astropy FITS header, to prepare for database insert
#

from datetime import datetime
import re


# Parse image meta data
# Args: astropy FITS header (dict)
# Returns: list of things
def parseImageMetaData(imageHeader):

	output = [None]*25

	#Extract correct sat id number from the MSB title, not the 'OBJECT' keyword
	msbRegex = re.search(r"^\d+", imageHeader.get('MSBTITLE'))
	if msbRegex is not None:
		satID = msbRegex.group()
	else:
		satID = "-1"

	output[0] = imageHeader.get('MSBTITLE')
	output[1] = imageHeader.get('TELESCOP')
	output[2] = imageHeader.get('INSTRUME')
	output[3] = satID
	output[4] = (lambda x: 'Sidereal' if 'Sidereal' in x else 'Target')(imageHeader.get('MSBTITLE'))
	output[5] = (lambda x: None if x is None else datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S.%f'))(imageHeader.get('DATE-OBS'))
	output[6] = (lambda x: None if x is None else datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S.%f'))(imageHeader.get('DATE-END'))
	output[7] = imageHeader.get('EXP_TIME')
	output[8] = imageHeader.get('FILTER')
	output[9] = imageHeader.get('CCD_TEMP')
	output[10] = imageHeader.get('AIRTEMP')
	output[11] = imageHeader.get('GAIN')
	output[12] = imageHeader.get('NREADS')
	output[13] = imageHeader.get('READMODE')
	output[14] = imageHeader.get('FOC_POSN')
	output[15] = imageHeader.get('TELRA')
	output[16] = imageHeader.get('TELDEC')
	output[17] = imageHeader.get('RARATE')
	output[18] = imageHeader.get('DECRATE')
	output[19] = imageHeader.get('AIRMASS')
	output[20] = imageHeader.get('DARK')
	output[21] = imageHeader.get('FLAT')
	output[22] = (lambda x: None if x is None else datetime.strptime(x, '%Y-%m-%d_%H:%M').strftime('%Y-%m-%d %H:%M:%S'))(imageHeader.get('REDUCED'))
	output[23] = (lambda x: None if x is None else datetime.strptime(x, '%Y-%m-%d_%H:%M').strftime('%Y-%m-%d %H:%M:%S'))(imageHeader.get('ASTRONOM'))
	output[24] = imageHeader.get('APRAD')

	return output


