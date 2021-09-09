# populateDB.py
#
# Populate the database with some or all of the things
#
# Call from command python3 populateDB.py <directory> <databaseFile>
# -i populate images
# -s populate sidereal reference star measurements
# -t populate target measurements
# -r populate target rejections
#

import argparse
import os
import sqlite3
from astropy.io import fits

from insertImage import insertImage
from insertReferenceStar import insertReferenceStar
from readPPOutput import readPPOutput
from insertTarget import insertTarget
from rejectTarget import rejectTarget
from computeAltAz import computeAltAz
from pickeringAirmass import pickeringAirmass

location = "UKIRT"

#######################################################################################################################

# Open a FITS file and extract data
# Args: filename = string
# Return: metadata dictionary, image data array
def openFITS(filename):
	hdul = fits.open(filename)
	header = hdul[0].header
	data = hdul[0].data
	hdul.close()
	return header, data


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



# Main function to dig through directories and populate the database with the things
# Args: directory = path, dbCursor = sqlite cursor, <flags to add things or not>
# Returns: nothing
def populateDB(directory, dbCursor, addImages=False, addSidereal=False, addTargets=False, addRejections=False):
	print("\n################################################################################\n")
	print("Checking everything in " + os.fsdecode(directory))

	# Iterate through files
	for file in os.listdir(directory):
		filename = os.fsdecode(file)

		# Check if sub-directory and enter if so
		if os.path.isdir(os.path.join(directory, file)):
			print("################################################################################")
			print("\n\"" + filename + "\" is a sub-directory, entering recursion level...\n")
			populateDB(os.path.join(directory, file), dbCursor, addImages, addSidereal, addTargets, addRejections)

		else:

			# Check if applicable image file
			if addImages and filename.endswith(".fits"):
				imageFile = filename

				print("_______________________________________________________________________________")
				print("Found image file \"" + imageFile + "\", checking contents...")

				#Open file
				try:
					header, data = openFITS(os.fsdecode(os.path.join(directory, os.fsencode(imageFile))))
				except Exception as e:
					appendLog(os.fsdecode(imageFile), "failed to open!")
					print("Failed to open!")
					print(e)
					continue

				#Add image to database
				try: 
					result = insertImage(dbCursor, imageFile, header)
					if result[0] < 1:
						raise Exception("Databse returned " + str(result) + " rows")
				except Exception as e:
					appendLog(os.fsdecode(imageFile), "failed to add to database!")
					print("Failed to add to database!")
					print(e)
					continue

				print("Added " + str(result[0]) + " images to database.")
				print("Added " + str(result[1]) + " satellites to database.")


			# Check if applicable reference star file
			if addSidereal and filename.endswith("photometry_Control_Star.dat"):
				ppSidFile = filename

				print("_______________________________________________________________________________")
				print("Found measurements file \"" + ppSidFile + "\", checking contents...")

				#Open file
				try:
					data = readPPOutput(os.fsdecode(os.path.join(directory, os.fsencode(ppSidFile))))
				except Exception as e:
					appendLog(os.fsdecode(ppSidFile), "failed to open!")
					print("Failed to open!")
					print(e)
					continue

				#Add measurements to database
				out = 0
				for i,m in data.iterrows():
					try:
						alt,az = computeAltAz(float(m['julian_date']), location, float(m['source_ra']), float(m['source_dec']))

						# print(m['source_extractor_flag'], type(m['source_extractor_flag'])) 
						temp = [m['filename'].replace(".ldac", ".fits"),
								m['photometric_catalog'],
								m['source_ra'],
								m['source_dec'],
								alt,
								az,
								pickeringAirmass(alt),
								m['inst_mag'],
								m['inst_mag_sig'],
								m['mag'],
								m['sig'],
								m['zeropoint'],
								m['zeropoint_sig'],
								m['FWHM'],
								m['source_extractor_flag'],
								(True if m['rejected'] == "#" or m['zeropoint'] == 0.0 or m['source_extractor_flag'] != 0 else False)]

						# Insert reference star data 
						result = insertReferenceStar(dbCursor, temp)

						if result < 1:
							raise Exception("Databse returned " + str(result) + " rows")

						out += result

					except Exception as e:
						appendLog(os.fsdecode(ppSidFile), "failed to add measurement to database!")
						print("Failed to add measurement to database!")
						print(e)
						continue

				print("Added " + str(out) + " photometric reference measurements to database.")


			# Check if applicable target measurements file
			if addTargets and filename.endswith("photometry_manual_target.dat"):
				ppTargetFile = filename

				print("_______________________________________________________________________________")
				print("Found measurements file \"" + ppTargetFile + "\", checking contents...")

				#Open file
				try:
					data = readPPOutput(os.fsdecode(os.path.join(directory, os.fsencode(ppTargetFile))))
				except Exception as e:
					appendLog(os.fsdecode(ppTargetFile), "failed to open!")
					print("Failed to open!")
					print(e)
					continue

				#Add measurements to database
				out = 0
				for i,m in data.iterrows():
					try: 
						temp = [m['filename'].replace(".ldac", ".fits"),
								m['filename'].replace(".ldac", ".fits"),
								m['source_ra'],
								m['source_dec'],
								m['inst_mag'],
								m['inst_mag_sig'],
								m['FWHM'],
								m['source_extractor_flag']]

						# Insert reference star data 
						result = insertTarget(dbCursor, temp)

						if result < 1:
							raise Exception("Databse returned " + str(result) + " rows")

						out += result

					except Exception as e:
						appendLog(os.fsdecode(ppTargetFile), "failed to add measurement to database!")
						print("Failed to add measurement to database!")
						print(e)
						continue

				print("Added " + str(out) + " target measurements to database.")


			# Check if applicable target rejections file
			if addRejections and filename.endswith("rejections.dat"):
				rejectionsFile = filename

				print("_______________________________________________________________________________")
				print("Found measurements file \"" + rejectionsFile + "\", checking contents...")

				#Open file
				try:
					f = open(os.fsdecode(os.path.join(directory, os.fsencode(rejectionsFile))), "r")
					data = f.readlines()
				except Exception as e:
					appendLog(os.fsdecode(rejectionsFile), "failed to open!")
					print("Failed to open!")
					print(e)
					continue

				#Add rejections to database
				out = 0
				for m in data:
					try: 
						m = m.strip()

						# Add rejection flag to measurement in database 
						result = rejectTarget(dbCursor, m)

						if result < 1:
							raise Exception("Databse returned " + str(result) + " rows")

						out += result

					except Exception as e:
						appendLog(os.fsdecode(rejectionsFile), "failed to add rejection to database!")
						print("Failed to add rejection to database!")
						print(e)
						continue

				print("Added " + str(out) + " target measurement rejections to database.")



#######################################################################################################################

parser = argparse.ArgumentParser()
parser.add_argument("directory", help="directory to start looking for files")
parser.add_argument("databaseFile", help="path to database file")
parser.add_argument("-i", "--images", help="populate database with all image files", action="store_true")
parser.add_argument("-s", "--sidereal", help="populate database with all sidereal measurements", action="store_true")
parser.add_argument("-t", "--targets", help="populate database with all target measurements", action="store_true")
parser.add_argument("-r", "--rejections", help="update databse with all target measurement rejections", action="store_true")


args = parser.parse_args()

createLog()
directory = os.fsencode(args.directory)
databaseFile = os.fsencode(args.databaseFile)
addImages = args.images
addSidereal = args.sidereal
addTargets = args.targets
addRejections = args.rejections



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
populateDB(directory, cursor, addImages, addSidereal, addTargets, addRejections)

#Commit changes to database
conn.commit()
conn.close()

