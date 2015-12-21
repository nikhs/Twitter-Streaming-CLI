import sqlite3
from sys import stderr

class Database(object):
	"""Manage db connections."""
	def __init__(self, dbname='tweets.db'):
		self.dbname = dbname
		self.connection = sqlite3.connect(self.dbname) # create db in folder with given name.
		self.connection.execute('''CREATE TABLE IF NOT EXISTS tweets \
	       (id TEXT PRIMARY KEY NOT NULL,
	       	user TEXT NOT NULL,
	       	tweet_count INT,
	       	tweet INT NOT NULL,
	       	links TEXT,
	       	created_at INT NOT NULL);''')
		# self.connection.execute('''DELETE FROM tweets''')
		stderr.write('Setup %s database\n'%(self.dbname))

	def insert(self, uid, user, tweet_count, tweet, links, created_at):
		with self.connection:
			cursor = self.connection.cursor()
			cursor.execute('''INSERT INTO tweets VALUES (?,?,?,?,?,?)''', [uid, user, tweet_count, tweet, links, created_at])

	def select(self, timestamp):
			cursor = self.connection.execute('''SELECT * FROM tweets where created_at>?''', (timestamp,))
			for row in cursor:
				yield row

	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):
		self.connection.close()
