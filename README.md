# site-collectd-plugin
Collectd Python plugin to find all matches of a regex on a site and return the final count of matches

## Dependencies
requests

## Install Instructions
1. Checkout this repository (e.g. `git clone https://github.com/harnitsignalfx/site-collectd-plugin`) somewhere on your system accessible by collectd. The suggested location is `/usr/share/collectd/`
2. Run the following command from within the newly created folder (site-collectd-plugin) `sudo pip install -r requirements.txt`
3. Create a configuration file or use the default one (10-site.conf) and place it under `/etc/collectd/managed_config/`


By default the configuration file tries to find the python file in the default location given under Step 1. But feel free to modify the location in Step 1 and make the same adjustment within the configuration file.

Variables within the configuration file - 
URL - should be a reachable destination (e.g. https://www.google.com) <br>
Regex - the Regex that the contents of the URL will be matched against. <br>
Interval - How frequently should the plugin poll (in seconds) the URL and try to match content + dispatch values. <br>
Timeout - How long to wait (in seconds) before we Timeout on the URL <br>
Name - Name of the metric that will be emitted. (The actual name will end up as 'gauge.Metric-Name') <br>
