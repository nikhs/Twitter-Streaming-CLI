import sys
from tweetstream import start_streaming, generate_content_report, generate_links_report, generate_user_report
import subprocess
from time import sleep


def showUsage():
	sys.stderr.write('\nUsage command.py <operation> [<arg>]\n')
	sys.stderr.write('where operation can be: stream or report\n\n')
	sys.stderr.write('stream: prints twitter streams to the console\n')
	sys.stderr.write('report: Generates reports based on the stream\n')
	sys.stderr.write('arg: space seperated list of phrases.\nReplace space in phrase with _ if needed, else every space seperated word is taken as seperate phrases.\n\n')
	sys.stderr.write('eg: to search for tweets with "the batman" include it here as "the_batman"(Without quotes)\n')
	sys.exit(0)

def parsearg(arguments):
	if not arguments:
		print 'No args provided. Obtaining general stream.'
		return ''

	arg = map(lambda word: word.replace('_', ' '), arguments)
	arg = ','.join(arg)

	print 'Tracking phrases: ', arg	
	return arg

def stop(operation, process=False):
	print 'Shutting Down. :('
	if operation == 'stream':
		sys.exit(1)
	else:
		process.terminate()
		sys.exit(1)

process = False

try:

	operation = sys.argv[1]

	if operation == 'stream':

		print 'Starting stream ....'
		arg = parsearg(sys.argv[2:])
		start_streaming(arg)

	elif operation == 'report':

		print 'Wait for report generation..'
		arg = parsearg(sys.argv[2:])
		process = subprocess.Popen(['python', 'worker.py', arg])

		# Wait for data to be mined 
		total_minutes_elapsed = 0

		while(True):

			seconds_elapsed = 0

			# Check if worker has ended
			streamdata = process.communicate()
			if process.returncode is  not None:
				sys.stderr.write('Worker died.')
				break

			print 'Wait 1 minute'
			while seconds_elapsed <60:
			
				# Check if worker has ended
				streamdata = process.communicate()
				if process.returncode is not None:
					sys.stderr.write('Worker died.')
					break

				sys.stderr.write('\n%d minutes %d seconds elapsed\n'%(total_minutes_elapsed, seconds_elapsed) )
				sys.stderr.flush()
				sleep(1)
				seconds_elapsed +=  1

			total_minutes_elapsed +=1

			minutes_ago = total_minutes_elapsed
			if total_minutes_elapsed > 5:
				minutes_ago = 5

			print 'Report for %d minutes(s) ago'%minutes_ago

			generate_content_report(minutes_ago)
			generate_links_report(minutes_ago)
			generate_user_report(minutes_ago)


	else:
		showUsage()

except IndexError:
	showUsage()
except KeyboardInterrupt:
	stop(operation, process)
except IOError:
	print 'Shutting Down. :('



