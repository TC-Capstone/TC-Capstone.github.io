'''This program is a youtube video downloader that is designed to couple to an offline voice assistant. 
	It can otherwise be slightly modified to function as a standalone downloader by ignoring anything related 
	to the tkinter library.  
'''

import requests
import os
import mysql.connector
from pytube import YouTube
from tkinter import *

downloadDirectory = "YoutubeDownloads"
databaseName = "CS499"
databasePassword = ""

databaseConnector = mysql.connector.connect(host = "localhost", user = "root", password = databasePassword, database = databaseName)
databaseCursor = databaseConnector.cursor(buffered=True)
tableName = downloadDirectory

# Makes certain we have a proper directory to write our files to.
def create_genre_directory(downloadDirectory):
	if not os.path.exists(downloadDirectory):
		print('Creating new directory \"' + downloadDirectory + "\"")
		os.makedirs(downloadDirectory)
	else: 
		print("Video download directory exists.")


# Only call this method when the proper download URL is stored in the clipboard first!
def download_video(downloadDirectory):
	#Also test copying other media not just text.
	create_genre_directory(downloadDirectory)
	try:
		YouTube(downloadURL).streams.first().download(output_path=downloadDirectory)
		InsertVideoToDatabase()
	except:
		print("Video had problems downloading, make sure URL was properly copied!")

# Checks if the video we download already exists in our database of saved videos and inserts a record if not.
def InsertVideoToDatabase():
	videoName = YouTube(downloadURL).title
	
	databaseCursor.execute("SELECT url FROM YoutubeDownloads")
	tableEntries = databaseCursor.fetchall()
	
	# Checking if any of the database entries match our current video.
	for url in tableEntries:
		urlStr = ''.join(url)
		if urlStr == downloadURL:
			print("Video already exists in database!")
			return

	insertVid = "INSERT INTO " + tableName + " (video_name, url) VALUES (%s, %s)"
	insertVals = (videoName, downloadURL)
	databaseCursor.execute(insertVid, insertVals)
	databaseConnector.commit()
	print("New row inserted to table!")

# Verifies that the database exists before we begin to perform operations on it.
def check_database_exists():
	databaseCursor.execute("SHOW DATABASES")

	databaseExistsCheck = False

	for database in databaseCursor.fetchall():
		# We convert the table tuple list to a string so it doesn't cause comparison issues. 
		databaseStr = ''.join(database)
		if (databaseStr == databaseName):
			databaseExistsCheck = True
			print("Database exists!")
			break;
	if databaseExistsCheck == False:
		databaseCursor.execute("CREATE DATABASE CS499")

	useDBStr = "USE " + databaseName 
	databaseCursor.execute(useDBStr)
	databaseConnector.commit()


def check_table_exists():
	useDBStr = "USE " + databaseName 
	databaseCursor.execute(useDBStr)
	databaseCursor.execute("SHOW TABLES")

	tableExistsBool = False

	for table in databaseCursor:
		# We convert the table tuple list to a string so it doesn't cause comparison issues. 
		tableStr = ''.join(table)
		if (tableStr == downloadDirectory):
			tableExistsBool = True
			print("Table exists!")
			return;

	if tableExistsBool == False:
		createTableStr = "CREATE TABLE " + tableName + " (id INT AUTO_INCREMENT PRIMARY KEY, video_name VARCHAR(254), url VARCHAR(254))"
		databaseCursor.execute(createTableStr)
		databaseConnector.commit()
		print("Table created!")


# Grabs the url stored in the clipboard first to minimize any potential errors.
downloadURL = Tk().clipboard_get()
check_database_exists()
check_table_exists()
print("Attempting to download the media contents found at " + downloadURL)
download_video(downloadDirectory)