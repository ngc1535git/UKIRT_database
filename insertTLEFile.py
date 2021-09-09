# insertTLEFile.py
#
# Load TLEs from a txt file and insert them into the database
#
# Call from command python3 insertTLEFile.py <txt file> <databaseFile>
#



import sys
import os
import argparse
import sqlite3

from insertTLE import insertTLE
from loadFile import loadAdamTLEFile


#######################################################################################################################

parser = argparse.ArgumentParser()
parser.add_argument("file", help="txt file of TLEs")
parser.add_argument("databaseFile", help="path to database file")


args = parser.parse_args()


file = os.fsencode(args.file)
databaseFile = os.fsencode(args.databaseFile)

# cwd = os.getcwd()
# file = "archived_TLE_catalog_new.txt"
# databaseFile = "test.db"



#######################################################################################################################

# Open database file (will create new one if not exist)
try:
	print("Opening database...")
	conn = sqlite3.connect(databaseFile)
except Exception as e:
	print("Failed!")
	print(e)
	exit()

print("Success!")

mycursor = conn.cursor()


#######################################################################################################################

#Load the list of TLEs from a file
print("\n################################################################################\n")
print("Loading TLEs from files...")

tleList = []


try: 
	tleList += loadAdamTLEFile(file)
except Exception as e:
	print("Could not load " + file)
	print(e)
	exit()


print("Loaded " + str(len(tleList)) + " TLEs.")




#######################################################################################################################

# Load TLEs into db
print("\n################################################################################\n")
print("Inserting TLE data into database...")

success = 0
sats = 0
fail = 0

for tle in tleList:
	try:
		out = insertTLE(mycursor, tle, "Spacetrack")
		sats += out[0]
		success += out[1]
		# print("Added ", success, "TLEs...")

	except Exception as e:
		print("Failed to add TLE!")
		print(e)
		fail += 1


print("Added %d new TLEs to the database." % success)
print("Added %d new sats to the database." % sats)
print("Failures = %d" % fail)

#######################################################################################################################

#Commit changes to database
conn.commit()
conn.close()
