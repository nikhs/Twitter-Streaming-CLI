import config
from sys import stderr
from twitstream import TwitStream

class Streamer(object):
	"""Interface to TwitStream object"""

	def __init__(self, track, headers):
		self.stream_handler = TwitStream(track)
		self.stream_handler.set_credentials(client_key= config.TW_KEY, client_secret= config.TW_SECRET,
			client_token= config.TW_TOKEN, client_token_secret= config.TW_TOKEN_SECRET)
		self.stream_handler.set_headers(headers)

	def __enter__(self):
		return self.stream_handler.stream()

	def __exit__(self, type, value, traceback):
		if isinstance(value, ValueError):
			stderr.write('Ignoring blank lines.')
			stderr.flush()
			return True
		elif isinstance(value, KeyError):
			stderr.write('Malformed data. Ignoring.')
			stderr.flush()
			return True

