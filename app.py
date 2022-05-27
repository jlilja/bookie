import os
import sys
import tempfile
import shutil
import sqlite3
import time
import yaml

# https://wiki.mozilla.org/images/d/d5/Places.sqlite.schema3.pdf
# https://stackoverflow.com/questions/464516/firefox-bookmarks-sqlite-structure

# https://askubuntu.com/questions/219234/firefox-unresponsive-due-to-lock-files-how-do-i-remove-them
# Here's a page about the lockfile. It needs to be removed before starting FF next time.
# Its probably why I have sooo much inconsistencies when developing.

# I found it. Its the file conveniently named 'lock'.
# So, when you run this script. Make sure to close down FF, delete the lock file, run this file, verify in a sql client.
# If you are lucky then the new bookmark(s) should be populated.
# Probably need to add a step to remove the lock file and check if there's an open FF session?

def getBookmarksFromFile():
	if not os.path.isfile('bookmarks.yml'):
		raise Exception('There is no bookmarks yml file')

	with open('bookmarks.yml') as fh:
	    return yaml.load(fh, Loader=yaml.FullLoader)

def getSqliteClient(profilePath):
	# pathToFile = findFirefoxDatabase()
	return sqlite3.connect(profilePath)

def addRecordToMozPlaces(profilePath, bookmark):
	url = bookmark['url']
	title = bookmark['title']

	try:
		client = getSqliteClient(profilePath)
		cursor = client.cursor()

		cursor.execute('''
			INSERT INTO
				moz_places
				(url, title)
			VALUES
				(?, ?)
			''',
			(url, title)
		)

		client.commit()
	except sqlite3.OperationalError as error:
		raise Exception('Database is locked. Is Firefox running?')

	return cursor.lastrowid

	pass

# table moz_bookmarks
# 	- id = auto incremental id
# 	- type = type 1 is bookmark, type 2 is folder
#	- fk = 1 to 1 relation to record in moz_places (null if folder)
#	- parent = IDK
#	- position = the position its placed in the folder
#	- title = name of bookmark

def addRecordToMozBookmarks(profilePath, bookmark, fk):
	bookmarkType = '1' if bookmark['type'] == 'bookmark' else '2'
	title = bookmark['title']
	timestamp = round(time.time() * 1000000)

	try:
		client = getSqliteClient(profilePath)
		cursor = client.cursor()

		cursor.execute('''
			INSERT INTO
				moz_bookmarks
				(type, fk, parent, title, position, dateAdded, lastModified)
			VALUES
				(?, ?, ?, ?, ?, ?, ?)
			''',
			(bookmarkType, fk, '3', title, 11, timestamp, timestamp)
		)
	except sqlite3.OperationalError as error:
		raise Exception('Database is locked. Is Firefox running?')

	client.commit()

	return cursor.lastrowid

def getProfilePath(profile):
	user = os.getlogin()
	file = 'places.sqlite'

	if profile:
		path = '/'.join(['/home', user, '.mozilla/firefox', profile, file])

		if not os.path.isfile(path):
			print('\nUnsure what profile your firefox is using? Browse to about:profiles and it will tell you.\n')

			raise Exception(f'There is no profile named %s' % profile)

		print(f'Profile %s found.' % profile)

		return path

	pass

if __name__ == '__main__':
	file = sys.argv[0]
	browser = sys.argv[1]
	profile = sys.argv[2]

	if browser not in ('firefox'):
		raise Exception(f'%s not in list of supported browsers' % browser)

	print(f'Looking for profile in %s directory' % browser)
	profilePath = getProfilePath(profile)
	print(f'Using path %s' % profilePath)

	bookmarks = getBookmarksFromFile()

	for bookmark in bookmarks['bookmarks']:
		fk = addRecordToMozPlaces(profilePath, bookmark)
		addRecordToMozBookmarks(profilePath, bookmark, fk)

	print('Done with sync')
