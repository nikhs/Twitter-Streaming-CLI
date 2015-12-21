from database import Database
from urlparse import urlparse
import re
from collections import Counter
from utility import unix_time_minutes_ago
from commonwords import common_words_list

# DB column indexes
UID = 0
USER = 1
TWEET_COUNT = 2
TWEET = 3
LINKS = 4
CREATED_AT = 5


def generate_user_report(minutes_ago):
	print 'User Report', '-'*20

	with Database() as db:
		for row in db.select(unix_time_minutes_ago(minutes_ago)):
			print  'User:',row[USER].encode('utf-8'), ', Total tweets:', row[TWEET_COUNT]

	print '-' * 32

def generate_links_report(minutes_ago):
	print 'Links Report', '-'*20

	links = []
	with Database() as db:
		for row in db.select(unix_time_minutes_ago(minutes_ago)):
			links += row[LINKS].split()
	print 'Total links shared:', len(links)

	_unique_domain_count(links)

	print '-' * 32

def generate_content_report(minutes_ago):
	print 'Content Report', '-'*20

	word_frequency = Counter()
	with Database() as db:
		for row in db.select(unix_time_minutes_ago(minutes_ago)):
			sanitised_line = _remove_common_words( _cleanup( _prepare_line(row[TWEET]) ) )
			word_frequency.update( _tokenize(sanitised_line) )
	
	print 'Total unique words:', len(word_frequency)
	print '10 Most common words'
	for word, count in  word_frequency.most_common(10):
		print word.encode('utf-8'),' -> ',count

	print '-' * 32

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

