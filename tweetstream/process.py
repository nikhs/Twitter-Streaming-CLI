
from streamer import Streamer
from database import Database
from json import loads
from utility import twitter_time_to_unix, twitter_time_to_local
from sys import stderr

def start_background_mining(track):
	""" initializes background mining of tweets. Stores them in a db.

	track -- comma seperated keywords to track

	"""
	with Database() as db:
		headers = {'User-Agent': ' Twitter Streaming CLI'}
		tweet_count = 0
		streamer = Streamer(track, headers)
		for line in streamer.start():
			with streamer.general_error_handler():
				tweet = loads(line)

				links = []
				for url in tweet['entities']['urls']:
					links.append(url['expanded_url'])
				links = ','.join(links) # comma seperated list of links

				db.insert(tweet['id_str'], tweet['user']['screen_name'],
				 tweet['user']['statuses_count'], tweet['text'], links, twitter_time_to_unix(tweet['created_at']))
				tweet_count += 1
				stderr.write('Processed %d tweet\n'%(tweet_count))


def start_streaming(track):
	""" Start streming tweets on the console

	 track -- comma seperated keywords to track

	 """

 	headers = {'User-Agent': ' Twitter Streaming CLI'}
	streamer = Streamer(track, headers)
	for line in streamer.start():
		with streamer.general_error_handler():
			tweet = loads(line)

			# Form data before printing to avoid incomplete output
			user = tweet['user']['screen_name'].encode('utf-8')
			text = tweet['text'].encode('utf-8')
			created_at = twitter_time_to_local(tweet['created_at'])

			print '-'*40
			print 'By: ', user
			print tweet['text'].encode('utf-8')
			print 'Created at', twitter_time_to_local(tweet['created_at'])

			print '-'*40

