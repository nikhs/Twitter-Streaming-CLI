import sys

def showUsage():
	sys.stderr.write('\nUsage command.py <operation> [<arg>]\n')
	sys.stderr.write('where operation can be: stream or report\n\n')
	sys.stderr.write('stream: prints twitter streams to the console\n')
	sys.stderr.write('report: Generates reports based on the stream\n')
	sys.stderr.write('arg: space seperated list of phrases.\nReplace space in phrase with _ if needed, else every space seperated word is taken as seperate phrases.\n\n')
	sys.stderr.write('eg: to search for tweets with "the batman" include it here as "the_batman"(Without quotes)\n')
	sys.exit(0)

try:
	operation = sys.argv[1]
	if operation == 'stream':
		print 'streaming'
	elif operation == 'report':
		arg = sys.argv[2:]
		print 'reporting'
		print ','.join(arg)
	elif operation == 'g':
		from time import sleep
		print 'sleeping..'
		sleep(10)
		print 'wokeup'
	else:
		showUsage()

except IndexError:
	showUsage()
except KeyboardInterrupt:
	print 'Shutting Down. :('




