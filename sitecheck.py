import collectd
import requests
import re
import collections

REGEX = ''
INTERVAL = 10
URL = ''
METRIC_NAME = ''
pattern = ''
TIMEOUT = 10

#Stat = collections.namedtuple('Stat', ('type', 'path')
#STATS_SITE = {
# 'site-results': Stat("gauge","site-results") 
#}

def config_callback(conf):

	for node in conf.children:
        	try:
            		if node.key == 'Regex':
            			global REGEX
                		REGEX = node.values[0]
            		elif node.key == 'Interval':
                		global INTERVAL
                		INTERVAL = node.values[0]
            		elif node.key == 'URL':
             		        global URL
                		URL = node.values[0]
            		elif node.key == 'Name':
                		global METRIC_NAME
                		METRIC_NAME = node.values[0]
            		elif node.key == 'Timeout':
                		global TIMEOUT
                		TIMEOUT = node.values[0]
        	except Exception as e:
            		collectd.error('Failed to load the configuration %s due to %s' % (node.key, e))
            		raise e

def init_callback():
	global pattern
	pattern = re.compile(REGEX,re.I)
	collectd.register_read(read_callback,interval=INTERVAL)

	collectd.notice('Matching pattern %s from URL %s and sending total matches as %s at a frequency of %s s' % (REGEX,URL,METRIC_NAME,INTERVAL))
	return True	

def read_callback():
	try:
		global pattern
		response = requests.get(URL,timeout=TIMEOUT)
		m = 0
		if response.status_code == 200:
			m = pattern.findall(response.content)
		collectd.notice('Matches - %s' % (m))
		val = collectd.Values()
		val.type =  'gauge'
		val.type_instance = METRIC_NAME
		val.plugin = 'site-regex-plugin'
		val.values = [len(m)]
		val.dispatch()
	except Exception as e:
		collectd.error('Failed to fetch and transfer data due to %s' % (e))

collectd.register_config(config_callback)
collectd.register_init(init_callback)
