# readPPOutput.py
#
# Reads the .dat output file from PP
#

import pandas as pd
import re
from io import StringIO


headers = ["rejected", "filename", "julian_date", "mag", "sig", "source_ra", "source_dec", "predicted_RA-source_RA", "predicted_Dec-source_Dec", "manual_offset_ra", "manual_offset_dec", "exposure", "zeropoint", "zeropoint_sig", "inst_mag", "inst_mag_sig", "photometric_catalog", "photometric_band", "source_extractor_flag", "telescope_instrument", "photometry_method", "FWHM"]


# Read the file from PP output
# Args: file = file path
# Returns: pandas dataframe
def readPPOutput(file):

	f = open(file, "r")
	raw = f.read()

	# Read file data, replacing whitespace with commas to include first column of rejection flags
	data = pd.read_csv(StringIO(re.sub("[ ]+", ",", raw)), header=0, names=headers)

	# print(temp)

	# Remove columns index
	data = data[:-10]

	# print(temp)

	return data




# file = 'photometry_Control_Star.dat'

# data = readPPOutput(file)

# print(data)

# #Add measurements to database
# out = 0
# for index, m in data.iterrows():
# 	temp = [m['filename'].replace(".ldac", ".fits"),
# 			m['photometric_catalog'],
# 			m['source_ra'],
# 			m['source_dec'],
# 			m['inst_mag'],
# 			m['inst_mag_sig'],
# 			m['mag'],
# 			m['sig'],
# 			m['zeropoint'],
# 			m['zeropoint_sig'],
# 			m['FWHM'],
# 			m['rejected']]

		
# print(temp)