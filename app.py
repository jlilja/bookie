import os
import tempfile
import shutil
import sqlite3
import time

# https://wiki.mozilla.org/images/d/d5/Places.sqlite.schema3.pdf
# https://stackoverflow.com/questions/464516/firefox-bookmarks-sqlite-structure

# https://askubuntu.com/questions/219234/firefox-unresponsive-due-to-lock-files-how-do-i-remove-them
# Here's a page about the lockfile. It needs to be removed before starting FF next time.
# Its probably why I have sooo much inconsistencies when developing.

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
	match = list(filter(lambda dir: dir.endswith(wantedSuffix), dirs))

	sqlitePath = '/'.join([basePath, match[0], file])

	if os.path.isfile(sqlitePath):
		print(f'Found sqlite file at {sqlitePath}')
		
		return sqlitePath

	print(f'Could not find Firefox sqlite file at {sqlitePath}')

if __name__ == '__main__':
	tmpdir = tempfile.gettempdir()
	# shutil.copy(os.path.join('/home/j/.mozilla/firefox/37rfrt13.default', "places.sqlite"), tmpdir)
	print(findFirefoxDatabase())
	conn = sqlite3.connect('places.sqlite')

	cursor = conn.cursor()

	# cursor.execute("""SELECT title FROM moz_bookmarks;""")
	# rows1 = cursor.fetchall()
	# print(rows1)

	timestamp = round(time.time() * 1000000)

	# print(timestamp)
	# print(time.time_ns())

	# cursor.execute("""UPDATE moz_bookmarks SET title = 'test' WHERE id = 123;""")
	cursor.execute( """INSERT INTO moz_bookmarks
                          (type, fk, parent, position, title, dateAdded) 
                           VALUES 
                          (1, 2707, 45, 5, 'och nu15', 1636148302936001)""")
	conn.commit()

	# cursor.execute("""SELECT title FROM moz_bookmarks;""")
	# rows2 = cursor.fetchall()



	# print(rows2)

	conn.close()

	print('done')
