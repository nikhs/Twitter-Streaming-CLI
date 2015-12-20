from requests import post
from requests_oauthlib import OAuth1

class TwitStream(object):
	"""Creates a handle for twitter streams."""

	ENDPOINT = 'https://stream.twitter.com/1.1/statuses/filter.json'

	def __init__(self, track):
		"""Set OAuth1 credentials.

		track -- Phrase(s) to track. Seperate multiple phrases with a comma.

		"""
		# Pass Default string if empty string provided.
		self.track = track.strip() or 'a' 
		self.oauth = None
		self.headers = None
		self.response = None

	def set_credentials(self, client_key, client_secret, client_token, client_token_secret):
		"""Set OAuth1 credentials.

		Keyword arguments
		client_key -- API client key
		client_secret -- API client secret
		client_token -- API access token
		client_token_secret -- API access token secret

		"""
		self.oauth = OAuth1(client_key, client_secret, client_token, client_token_secret)

	def set_headers(self, headers):
		""" Set custom headers (including User-Agent).

		headers -- Dict containing headers

		"""
		if isinstance(headers, dict):
			self.headers = headers
		else:
			raise TypeError('headers passed should be dict.')

	def stream(self):
		""" Generator for twitter stream."""
		if self.oauth is None:
			raise TypeError('Twitter API credentials not set')

		self.response = post(TwitStream.ENDPOINT, auth = self.oauth, 
			data={'track':self.track}, headers = self.headers, stream = True)
		
		for line in self.response.iter_lines():
			if line:
				yield line

if __name__ == '__main__':
	import config
	from json import loads
	from utility import twitter_time_to_local
	stream_handler = TwitStream(' d')
	stream_handler.set_credentials(client_key= config.TW_KEY, client_secret= config.TW_SECRET,
	 client_token= config.TW_TOKEN, client_token_secret= config.TW_TOKEN_SECRET)
	stream_handler.set_headers({'user-agent':'testing'})
	for line in stream_handler.stream():
		try:
			tweet = loads(line)
			print '-'*40
			print 'By: ', tweet['user']['screen_name'].encode('utf-8')
			print tweet['text'].encode('utf-8')
			print 'Created at', twitter_time_to_local(tweet['created_at'])

			print '-'*40
		except ValueError:
			print 'argh'
		except KeyError:
			print 'groan'
