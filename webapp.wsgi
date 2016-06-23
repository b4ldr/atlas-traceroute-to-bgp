import sys
import site
import logging
site.addsitedir('/srv/www/bgp-analyze.dns.icann.org/lib/python2.7/site-packages')
sys.path.insert(0, "/srv/www/bgp-analyze.dns.icann.org")
sys.path.insert(0, "/srv/www/bgp-analyze.dns.icann.org/lib/python2.7/site-packages")
from web import app as application

logging.captureWarnings(True)
handler = RotatingFileHandler(
  '/srv/www/bgp-analyze.dns.icann.org/app.log', maxBytes=10000,backupCount=1)
handler.setLevel(logging.DEBUG)
