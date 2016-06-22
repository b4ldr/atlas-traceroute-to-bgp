import sys
import site
site.addsitedir('/srv/www/bgp-analyze.dns.icann.org/lib/python2.7/site-packages')
sys.path.insert(0, "/srv/www/bgp-analyze.dns.icann.org")
sys.path.insert(0, "/srv/www/bgp-analyze.dns.icann.org/lib/python2.7/site-packages")
from web import app as application
