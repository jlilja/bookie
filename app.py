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

# table moz_bookmarks
# 	- id = auto incremental id
# 	- type = type 1 is bookmark, type 2 is folder
#	- fk = 1 to 1 relation to record in moz_places (null if folder)
#	- parent = IDK
#	- position = the position its placed in the folder
#	- title = name of bookmark

def findFirefoxDatabase():
	basePath = '/home/j/.mozilla/firefox'
	wantedSuffix = '.default'
	file = 'places.sqlite'

	dirs = os.listdir(basePath)
	getProfileMatches = lambda dir: dir.endswith('.default') or dir.endswith('.default-release')
	matches = list(filter(getProfileMatches, dirs))

	# Unsure what profile your firefox is using? Browse to about:profiles and it'll tell you.
	# TODO: Either parse the current profile, or add a drop down menu to select which one you want.
	print(f'Found {len(matches)} profile(s). Which one do you want? {matches}')

	myTemporaryProfile = 'key5ypi1.default-release'

	sqlitePath = '/'.join([basePath, myTemporaryProfile, file])

	if os.path.isfile(sqlitePath):
		print(f'Found sqlite file at {sqlitePath}')

		return sqlitePath

	print(f'Could not find Firefox sqlite file at {sqlitePath}')

def getBookmarksFromFile():
	if not os.path.isfile('bookmarks.yml'):
		print(f'There is no bookmarks yml file.')

		return False

	with open('bookmarks.yml') as fh:
	    return yaml.load(fh, Loader=yaml.FullLoader)

def getSqliteClient():
	pathToFile = findFirefoxDatabase()
	return sqlite3.connect(pathToFile)

def addRecordToMozPlaces(bookmark):
	client = getSqliteClient()
	cursor = client.cursor()

	url = bookmark['url']
	title = bookmark['title']

	cursor.execute('INSERT INTO moz_places (url, title) VALUES (?, ?)', (url, title))
	client.commit()

	return cursor.lastrowid

	pass

def addRecordToMozBookmarks(bookmark, fk):
	client = getSqliteClient()
	cursor = client.cursor()

	title = bookmark['title']

	timestamp = round(time.time() * 1000000)

	print(timestamp)

	# cursor.execute('INSERT INTO moz_bookmarks (type, fk, parent, title, position) VALUES (?, ?, ?, ?, ?)', ('1', fk, '3', title, 11))
	client.commit()

	return cursor.lastrowid

	pass

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

	# timestamp = round(time.time() * 1000000)

	# bookmarks = getBookmarksFromFile()

	# for bookmark in bookmarks['bookmarks']:
	# 	fk = addRecordToMozPlaces(bookmark)
	# 	addRecordToMozBookmarks(bookmark, fk)

	# print('Done with sync')
