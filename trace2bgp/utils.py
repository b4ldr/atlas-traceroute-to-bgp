import logging
from pyasn import pyasn
from cymruwhois import Client
from ripe.atlas.sagan import Result, TracerouteResult
from ripe.atlas.cousteau import AtlasLatestRequest

def get_sagan_objects(cousteau_object):
    '''ensure we only use traceroute results'''
    sagan_objects = []
    for result in cousteau_object:
        sagan_object = Result.get(result)
        if type(sagan_object) != TracerouteResult:
            logging.warning('{} is {} not TracerouteResult'.format(
                sagan_object, type(sagan_object)))
            continue
        logging.debug('Adding: {}'.format(sagan_object))
        sagan_objects.append(sagan_object)
    return sagan_objects

def get_cousteau_object(msm_id):
    '''return the cousteau object'''
    is_success, cousteau_object = AtlasLatestRequest(msm_id).get()
    if not is_success:
        logging.error('unable to process {} with cousteau'.format(msm_id))
        return None
    return cousteau_object
class Lookup(object):

    asndb = None
    def __init__(self, pyasn_file=None):
        if pyasn_file:
            self.asndb = pyasn(pyasn_file)
        self.whois = Client()

    def lookup(self, ip):
        if self.asndb:
            asn = self.asndb.lookup(ip)[0]
            if asn:
                return str(asn)
        else:
            return self.whois.lookup(ip).asn
