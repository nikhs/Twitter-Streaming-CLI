import datetime
import pytz
from tzlocal import get_localzone

def unix_time_minutes_ago(minutes):
	now = datetime.datetime.utcnow()
	ago = datetime.timedelta(minutes=minutes) # minutes duration object
	time_minutes_ago = now - ago
	return datetime_to_unix(time_minutes_ago)

def datetime_to_unix(dt):
	epoch = datetime.datetime.utcfromtimestamp(0)
	delta =  dt-epoch
	return int(delta.total_seconds() * 1000.00)

def twitter_time_to_unix(twitter_time):
	dt = datetime.datetime.strptime(twitter_time,'%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=None)
	return datetime_to_unix(dt)

def twitter_time_to_local(twitter_time):
	local_tz = get_localzone()
	utc_dt = datetime.datetime.strptime(twitter_time,'%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=None)
	local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
	return local_dt
