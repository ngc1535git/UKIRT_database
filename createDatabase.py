# createTables.py
#
# Opens database file (or creates new one if not exists) and creates the tables as specified in a separate .sql file
#
# WARNING!!!
# This script will delete any existing tables and data
#


import sqlite3


databaseFileName = "ukirt.db"
schemaFileName = "schema.sql"

#######################################################################################################################

# Read schema file
try:
	print("Reading schema file...")
	fstream = open(schemaFileName, "r")
	schema = fstream.read()
except Exception as e:
	print ("Failed!")
	print(e)
	exit()

print("Success!")

# print(schema)

# Open database file (will create new one if not exist)
try:
	print("Opening database...")
	conn = sqlite3.connect(databaseFileName)
except Exception as e:
	print("Failed!")
	print(e)
	exit()

print("Success!")

# Exceute SQL code to create tables
try:
	conn.executescript(schema)
except Exception as e:
	print("Failed!")
	print(e)
	exit()

print("Success!")

# Close database
conn.close()

print("Done!")	

