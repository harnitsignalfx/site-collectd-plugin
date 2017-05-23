import collectd
import requests
import re
import collections
import time

REGEX = ''
INTERVAL = 10
URL = ''
METRIC_NAME = ''
pattern = ''
TIMEOUT = 10

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

	#collectd.info('Matching pattern %s from URL %s and sending total matches as %s at a frequency of %s s' % (REGEX,URL,METRIC_NAME,INTERVAL))
	return True	

def read_callback():
	try:
		global pattern
		
		startTime = time.time()
		response = requests.get(URL,timeout=TIMEOUT)
		roundtripTime = time.time() - startTime

		m = 0
		if response.status_code == 200:
			m = pattern.findall(response.content)
		#collectd.info('Matches - %s' % (m))

		# Metric Names to be sent (# of Matches, Status Code, Server Response Time, Client Response Time)
		stats = [METRIC_NAME+'.content_matches',METRIC_NAME+'.status_code',METRIC_NAME+'.server_response_time',METRIC_NAME+'.client_response_time']
		# Values = # of Matches, Status Code, Server Response Time, Client Response Time
		if response.status_code == 200:
			values = [len(m),response.status_code,response.elapsed.total_seconds(),roundtripTime]
		else:
			values = [-1,response.status_code,0,0]

		for idx, value in enumerate(values):
			dispatch_values(stats[idx],value)

	except Exception as e:
		collectd.error('Failed to fetch and transfer data due to %s' % (e))

def dispatch_values(type_instance,values):
	val = collectd.Values(type='gauge')
	val.type_instance = type_instance
	val.plugin = 'site-regex-plugin'
	val.values = [values]
	#collectd.info('type_instance %s , values -> %s , val -> %s' %(type_instance,values,val))
	val.dispatch()

collectd.register_config(config_callback)
collectd.register_init(init_callback)