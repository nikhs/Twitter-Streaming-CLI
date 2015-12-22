# Built-in
from sys import stderr, exit, argv
from json import loads
from time import time
from urlparse import urlparse
from collections import Counter
from httplib import IncompleteRead
import re
import datetime
import pytz
import sqlite3

# 3rd Party
from requests import post
from requests_oauthlib import OAuth1
from requests import RequestException
from tzlocal import get_localzone

# Data Files
from config import *
from commonwords import common_words_list

# Handle db connections
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
		stderr.write('\nConnecting to %s database\n'%(self.dbname))

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

# Time handling helper functions

def datetime_to_unix(dt):
	epoch = datetime.datetime.utcfromtimestamp(0)
	delta =  dt-epoch
	return int(delta.total_seconds() * 1000.00)

def twitter_time_to_unix(twitter_time):
	dt = datetime.datetime.strptime(twitter_time,'%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=None)
	return datetime_to_unix(dt)

# Twitter stream processing
def stream(db, track):
	
	ENDPOINT = 'https://stream.twitter.com/1.1/statuses/filter.json'

	oauth = OAuth1(TW_KEY, TW_SECRET, TW_TOKEN, TW_TOKEN_SECRET)
	headers = {'User-Agent': 'Twitter CLI'}
	response = post(ENDPOINT, auth=oauth, data={'track':track}, headers= headers, stream= True)

	tweet_count = 0
	running = True
	start = time()
	while running:
		try:
			for line in response.iter_lines():

				elapsed =  time() - start
				if elapsed >= 60:
					break

				if line:
					try:
						tweet = loads(line)

						links = []
						for url in tweet['entities']['urls']:
							links.append(url['expanded_url'])
						links = ','.join(links) # comma seperated list of links

						db.insert(tweet['id_str'], tweet['user']['screen_name'],
						 tweet['user']['statuses_count'], tweet['text'], links, twitter_time_to_unix(tweet['created_at']))
						tweet_count += 1

						stderr.write('\r')
						stderr.write('%d seconds elapsed, %d tweets stored'%(elapsed, tweet_count))
						stderr.flush()

					except KeyError:
						continue
					except ValueError:
						# stderr.write('Invalid')
						# stderr.write(line)
						continue
		except RequestException:
			continue
		except IncompleteRead:
			# stderr.write('Issues in request/response')
			continue

		running = False

# Generate required reports
def generate_reports(db, minutes_ago):

	# DB column indexes
	UID = 0
	USER = 1
	TWEET_COUNT = 2
	TWEET = 3
	LINKS = 4
	CREATED_AT = 5

	# HELPER Internal Functions

	def _unique_domain_count(list_of_links):
		
		domain_list = map(lambda uri: urlparse(uri).netloc, list_of_links)
		domain_counts = Counter(domain_list)
		print 'Unique domain counts'
		for domain, count in domain_counts.most_common()[:]:
			print domain, ' -> ', count


	def _prepare_line(line):
		return line.lower()

	def _remove_common_words(line):
		return filter(lambda word:word not in common_words_list, line.split())


	def _cleanup(line):
		link_ptr = r'\[.*?\)'
		url_ptr = r'(http|ftp).*? '
		rest_ptr = r'[\^\p{L}]'
		filtered_line =  re.sub(link_ptr,"",line)
		filtered_line =  re.sub(rest_ptr,"",filtered_line)
		filtered_line =  re.sub(url_ptr,"",filtered_line)
		return filtered_line.strip()

	def _tokenize(line):
		word_list = []
		for word in line:
			word_list.append(word)
		return word_list 


# Begin REPORT PROCESSING

	minutes_ago_dt = datetime.datetime.now() - datetime.timedelta(minutes=minutes_ago)
	minutes_ago_unix = datetime_to_unix(minutes_ago_dt)

	links =[]
	word_frequency = Counter()

# Seperator
	print '\n\n','*'*30,'\n\n'
# User Report Header
	print '\nUser Report', '-'*20,'\n'
	for row in db.select(minutes_ago_unix):
		user = row[USER]
		tweets_count = row[TWEET_COUNT]
		links += row[LINKS].split()
		tweet_text = row[TWEET]

	# Generate User Report
		print  'User:',user.encode('utf-8'), ', Total tweets:', tweets_count

	# Word Frequency Operation
		sanitised_line = _remove_common_words( _cleanup( _prepare_line(row[TWEET]) ) )
		word_frequency.update(_tokenize(sanitised_line))

# End User Report
	print '-' * 32

# Seperator
	print '\n\n','*'*30,'\n\n'
# Generate Links Report
	print '\nLinks Report', '-'*20,'\n'
	_unique_domain_count(links)
	print '-' * 32	

# Seperator
	print '\n\n','*'*30,'\n\n'
# Content Report
	print 'Content Report', '-'*20,'\n'
	print 'Total unique words:', len(word_frequency)
	print '10 Most common words'
	for word, count in  word_frequency.most_common(10):
		print word.encode('utf-8'),' -> ',count
	print '-' * 32

# End REPORTS

# Encapsulate mining and report generation
def process(track='tweet'):
	minutes = 0
	try:
		while True:
			with Database() as db:
				stream(db, track)
				minutes+= 1
				stderr.write('\Generating Reports...')

				minutes_ago = minutes
				if minutes_ago > 5:
					minutes_ago = 5

				#Generate report
				print '\nReports for tweets obtained %d minutes ago\n'%minutes_ago
				print '-'* 30
				print '-'* 30
				print 
				generate_reports(db, minutes_ago)
				print '\n\n','*'*30,'\n','*'*30,'\n'

	except KeyboardInterrupt:
		stderr.write('\n\nShutting Down!!!')

# Show command usage
def showUsage():
	stderr.write('\nUsage stream.py <track_args>\n')
	stderr.write('track_args: space seperated list of phrases.\nReplace space in phrase with _ if needed, else every space seperated word is taken as seperate phrases.\n\n')
	stderr.write('eg: to search for tweets with "the batman" include it here as "the_batman"(Without quotes)\n')
	exit(1)

# Store track fields and process
def main():
	try:
		# Obtain input track phrases
		if argv[1]:
			track = map(lambda word: word.replace('_', ' '), argv[1:])
			track = ','.join(track)

			process(track)

	except IndexError:
		showUsage()
		exit(1)

if __name__ == '__main__':
	main()