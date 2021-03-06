import os
import sys
import sqlite3
import time
import yaml
import random, string

# https://wiki.mozilla.org/images/d/d5/Places.sqlite.schema3.pdf
# https://stackoverflow.com/questions/464516/firefox-bookmarks-sqlite-structure

# https://askubuntu.com/questions/219234/firefox-unresponsive-due-to-lock-files-how-do-i-remove-them
# Here's a page about the lockfile. It needs to be removed before starting FF next time.
# Its probably why I have sooo much inconsistencies when developing.

# I found it. Its the file conveniently named 'lock'.
# So, when you run this script. Make sure to close down FF, delete the lock file, run this file, verify in a sql client.
# If you are lucky then the new bookmark(s) should be populated.
# Probably need to add a step to remove the lock file and check if there's an open FF session?

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def getBookmarksFromFile():
	if not os.path.isfile('bookmarks-example.yml'):
		raise Exception('There is no bookmarks yml file')

	with open('bookmarks-example.yml') as fh:
	    return yaml.load(fh, Loader=yaml.FullLoader)

def runSqlQuery(profilePath, query, values):
	client = sqlite3.connect(profilePath)

	try:
		cursor = client.cursor()
		cursor.execute(query, values)
		client.commit()
	except sqlite3.OperationalError as error:
		raise Exception('Database is locked. Is Firefox running?')

	return cursor.lastrowid

def addRecordToMozPlaces(profilePath, bookmark):
	url = bookmark['url']
	title = bookmark['title']
	guid = randomword(10)

	return runSqlQuery(profilePath, '''
		INSERT INTO
			moz_places
				(url, title, guid)
		VALUES
			(?, ?, ?)
		''', (url, title, guid)
	)

def bookmarkOrFolder(record):
	mapping = {
		'bookmark': '1',
		'folder': '2'
	}

	return mapping[record['type']]

# table moz_bookmarks
# 	- id = auto incremental id
# 	- type = type 1 is bookmark, type 2 is folder
#	- fk = 1 to 1 relation to record in moz_places (null if folder)
#	- parent = 3 if it is a top level bookmark. Otherwise the id of the folder it belongs to.
#	- position = the position its placed in the folder
#	- title = name of bookmark

def addBookmarkToMozBookmarks(profilePath, bookmark, fk, parent):
	bookmarkType = bookmarkOrFolder(bookmark)
	title = bookmark['title']
	timestamp = round(time.time() * 1000000)
	guid = randomword(10)

	return runSqlQuery(profilePath, '''
		INSERT INTO
			moz_bookmarks
				(type, fk, parent, title, position, dateAdded, lastModified, guid)
		VALUES
			(?, ?, ?, ?, ?, ?, ?, ?)
		''', (bookmarkType, fk, parent, title, 11, timestamp, timestamp, guid)
		)


def addFolderToMozBookmarks(profilePath, record, parent):
	bookmarkType = bookmarkOrFolder(record)
	title = record['title']
	timestamp = round(time.time() * 1000000)
	guid = randomword(10)

	return runSqlQuery(profilePath, '''
		INSERT INTO
			moz_bookmarks
				(type, parent, title, position, dateAdded, lastModified, guid)
		VALUES
			(?, ?, ?, ?, ?, ?, ?)
		''', (bookmarkType, parent, title, 11, timestamp, timestamp, guid)
	)

def getProfilePath(profile):
	user = os.getlogin()
	file = 'places.sqlite'

	if profile:
		path = '/'.join(['/home', user, '.mozilla/firefox', profile, file])

		if not os.path.isfile(path):
			print('\nBrowse to about:profiles and it will tell you.\n')
			raise Exception(f'There is no profile named %s' % profile)

		print(f'Profile %s found.' % profile)

		return path

	pass

def addBookmarkLoop(records, parent):
	for record in records:
		if record['type'] == 'bookmark':
			fk = addRecordToMozPlaces(profilePath, record)
			addBookmarkToMozBookmarks(profilePath, record, fk, parent)

		if record['type'] == 'folder':
			newParent = addFolderToMozBookmarks(profilePath, record, parent)

			if record['children']:
				addBookmarkLoop(record['children'], newParent)

if __name__ == '__main__':
	browser = sys.argv[1]
	profile = sys.argv[2]

	if browser not in ('firefox'):
		raise Exception(f'%s not in list of supported browsers' % browser)

	print(f'Looking for profile in %s directory' % browser)
	profilePath = getProfilePath(profile)
	print(f'Using path %s' % profilePath)

	records = getBookmarksFromFile()
	addBookmarkLoop(records['bookmarks'], '3')

	print('Done with sync')
