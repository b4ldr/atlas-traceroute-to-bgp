import logging
from typing import List, Optional

from cymruwhois import Client  # type: ignore
from pyasn import pyasn  # type: ignore
from ripe.atlas.cousteau import AtlasLatestRequest  # type: ignore
from ripe.atlas.sagan import Result, TracerouteResult  # type: ignore


def get_sagan_objects(cousteau_object: str) -> List[TracerouteResult]:
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

def get_cousteau_object(msm_id: int) -> Optional[str]:
    '''return the cousteau object'''
    is_success, cousteau_object = AtlasLatestRequest(msm_id).get() # type: ignore
    if not is_success:
        logging.error('unable to process {} with cousteau'.format(msm_id))
        return None
    return cousteau_object # type: ignore
class Lookup(object):

    asndb = None
    def __init__(self, pyasn_file: Optional[str]=None):
        if pyasn_file:
            self.asndb = pyasn(pyasn_file)
        self.whois = Client()

    def lookup(self, ip: str) -> Optional[str]:
        if self.asndb:
            asn = self.asndb.lookup(ip)[0]
            if asn:
                return str(asn)
        else:
            return self.whois.lookup(ip).asn
