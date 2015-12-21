from requests import post
from requests_oauthlib import OAuth1
from httplib import IncompleteRead
from requests import RequestException
from sys import stderr, exit

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
		
		try:
			for line in self.response.iter_lines():
				if line:
					yield line
		except IncompleteRead:
			stderr.write('\HTTP Error. Network gave incorrrect reponse. FATAL. Exiting.\n')
			exit(1)
		except RequestException:
			stderr.write('\nGeneral Network error. FATAL. Exiting.\n')
			exit(1)