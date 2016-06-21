#!/usr/bin/env python

from requests import get
import logging
from trace2bgp.utils import Lookup

class Asn(object):
    '''object to hold a single asn and its paths'''
    def __init__(self, id, original_path):
        self.orginal_path    = original_path
        self.id              = id
        self.paths           = set()
        self.downstream_asns = set()
        self.transit_asns    = set()

    @property
    def min_path_len(self):
        return min(map(len, self.paths))

    @property
    def max_path_len(self):
        return min(map(len, self.paths))

class Asns(object):
    '''object to hold a collection of ASNs'''
    asndb = None

    def __init__(self, sagan_objects, pyasn_file=None):
        lookup                = Lookup(pyasn_file)
        self.lookup           = lookup.lookup
        self.logger           = logging.getLogger('trace2bgp.atlas.asns')
        self.sagan_objects    = sagan_objects
        self._asns            = []
        self._asn_paths       = []

    def __len__(self):
        return len(self.asn_paths)

    @staticmethod
    def _remove_prepends(path):
        #http://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order
        seen     = set()
        seen_add = seen.add
        return tuple([x for x in path if not(x in seen or seen_add(x))])
    
    def lookup(self, ip):
        if self.asndb:
            asn = self.asndb.lookup(ip)[0]
            if asn:
                return str(asn)
        else:
            return self.whois.lookup(ip).asn

    @property
    def asns(self):
        '''sort through an array of paths and creat a dictionary of bgp paths.
        the key equals the starting asn and the value is a set of paths seen for
        that asn'''
        if self._asns:
            return self._asns
        asns = dict()
        for asn_path in self.asn_paths:
            full_path = self._remove_prepends(asn_path)
            self.logger.info('processing path: {}'.format(full_path))
            for asn in full_path:
                if asn == full_path[-1]:
                    break
                path = full_path[full_path.index(asn):]
                self.logger.debug('adding new ASN({}) with path: {}'.format(asn, path))
                if asn not in asns:
                    asns[asn] = Asn(asn, full_path)
                asns[asn].paths.add(path)
                asns[asn].transit_asns.add(full_path[full_path.index(asn) + 1])
                if asn != full_path[0]:
                    asns[asn].downstream_asns |= set(full_path[:full_path.index(asn)])
        #for asn in asns.values():
        #    self.logger.debug('found the following path: {} - {}'.format(
        #        asn.id, asn.paths))
        self._asns = asns.values()
        return self._asns

    @property
    def asn_paths(self):
        '''sort throught traceroute results.  it converts
        the ip address of each hop in the traceroute to create
        an as hop path.'''
        if self._asn_paths:
            return self._asn_paths
        asn_paths = []
        for result in self.sagan_objects:
            if result.is_error:
                self.logger.error('{}: {}'.format(result, result.error_message))
                continue
            if not result.source_address:
                self.logger.warning('No source address for {}'.format(result))
                continue
            asn_path = []
            self.logger.debug('Checking: {}'.format(result.source_address))
            msm_asn = self.lookup(result.source_address)
            if msm_asn:
                self.logger.debug('Adding: {}'.format(msm_asn))
                asn_path.append(msm_asn)
            for hop in result.hops:
                for packet in hop.packets:
                    if packet.origin:
                        self.logger.debug('Checking: {}'.format(packet.origin))
                        asn = self.lookup(packet.origin)
                        if asn and asn != asn[-1]:
                            self.logger.debug('Adding: {}'.format(asn))
                            asn_path.append(asn)
                        break
            self.logger.info('Found path: {}'.format(asn_path))
            asn_paths.append(asn_path)
        self._asn_paths = asn_paths
        return self._asn_paths
