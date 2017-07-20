# site-content-match
Collectd Python plugin to find all matches of a regex on a site and return the final count of matches



## Install Instructions
1. Checkout this repository somewhere on your system accessible by collectd. The suggested location is `/usr/share/collectd/`
2. Run the following command from the directory folder in Step 1 `sudo pip install -r requirements.txt`
3. Create a configuration file or use the default one (10-site.conf) and place it under `/etc/collectd/managed_config/`


By default the configuration file tries to find the python file in the default location given under Step 1. But feel free to modify the location in Step 1 and make the same adjustment within the configuration file.

Variables within the configuration file - 
URL - should be a reachable destination (e.g. https://www.google.com) <br>
Regex - the Regex that the contents of the URL will be matched against. <br>
Interval - How frequently should the plugin poll (in seconds) the URL and try to match content + dispatch values. <br>
Timeout - How long to wait (in seconds) before we Timeout on the URL <br>
Name - Name of the metric that will be emitted. (The actual name will end up as 'gauge.Metric-Name') <br>
