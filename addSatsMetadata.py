# addSatsMetadata.py
#
# Add metadata to database
#
# Call from command python3 addSatsMetadata.py <databaseFile>



import sqlite3
from satMetadata import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("databaseFile", help="path to database file")

args = parser.parse_args()

# Open database file (will create new one if not exist)
try:
	print("Opening database...")
	conn = sqlite3.connect(args.databaseFile)
except Exception as e:
	print("Failed!")
	print(e)
	exit()

print("Success!")


# Cursor for accessing the DB
cursor = conn.cursor()


def addSatMetadata(cursor, norad, name, satType, launch):
	sql = "UPDATE sats SET name = ?, type = ?, launch = strftime('%Y-%m-%d', ?) WHERE norad_id = ?;"
	cursor.execute(sql, [name, satType, launch, norad])

	targetUpdated = cursor.rowcount
	print("Updated", targetUpdated, "sats!")




for key, value in satMetadata.items():
	# print(key, value)
	addSatMetadata(cursor, key, *value)


# Commit changes to database and close
conn.commit()
conn.close()