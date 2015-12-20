import config
from sys import stderr
from twitstream import TwitStream
from contextlib import contextmanager

class Streamer(object):
	"""Interface to TwitStream object"""

	def __init__(self, track, headers):
		self.stream_handler = TwitStream(track)
		self.stream_handler.set_credentials(client_key= config.TW_KEY, client_secret= config.TW_SECRET,
			client_token= config.TW_TOKEN, client_token_secret= config.TW_TOKEN_SECRET)
		self.stream_handler.set_headers(headers)

	@contextmanager
	def general_error_handler(self):
		try:
			yield
		except ValueError:
			stderr.write('\nIgnoring blank lines.\n')
			pass
		except KeyError:
			stderr.write('\nMalformed data. Ignoring.\n')
			pass

	def start(self):
		return self.stream_handler.stream()
