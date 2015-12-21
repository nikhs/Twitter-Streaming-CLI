from tweetstream import start_background_mining
import signal
import sys

def stop(signal, frame):
	sys.stderr.write('Closing DB. Exiting worker.')
	sys.exit(0)

signal.signal(signal.SIGTERM, stop)
signal.signal(signal.SIGINT, stop)

try:

	# Obtain input	
	try:
		track = sys.argv[1] or sys.argv[1:]
		track = ','.join(track)
	except IndexError:
		sys.stderr.write('No arguments provided. Starting without track fields.')
		track = ''

	start_background_mining(track)
		
except KeyboardInterrupt:
	pass
except IOError:
	pass



