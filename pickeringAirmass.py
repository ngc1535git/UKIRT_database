# pickeringAirmass.py
#

import numpy as np

# Calculate airmass, https://en.wikipedia.org/wiki/Air_mass_(astronomy)
# Args: altitude = num
# Returns: num
def pickeringAirmass(altitude):
	return 1/(np.sin(np.radians(altitude + 244/(165 + 47*altitude**1.1))))