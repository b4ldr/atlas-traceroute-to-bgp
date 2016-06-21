#!/usr/bin/env python

import logging
from trace2bgp.atlas import Asn, Asns
from trace2bgp.utils import get_sagan_objects, get_cousteau_object
from prettytable import PrettyTable
from argparse import ArgumentParser
from ripe.atlas.cousteau import AtlasLatestRequest

def get_args():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--verbose', action='count' )
    parser.add_argument('--pyasn-file')
    parser.add_argument('msm_id')
    return parser.parse_args()

def set_log_level(args_level):
    log_level = logging.ERROR
    lib_log_level = logging.ERROR
    if args_level == 1:
        log_level = logging.WARN
    elif args_level == 2:
        log_level = logging.INFO
        lib_log_level = logging.WARN
    elif args_level == 3:
        log_level = logging.DEBUG
    elif args_level > 3:
        lib_log_level = logging.DEBUG
    logging.basicConfig(level=log_level)
    logging.getLogger('requests').setLevel(lib_log_level)
    logging.getLogger('urllib3').setLevel(lib_log_level)

def report(headings, entries, sortby=None, reversesort=False):
    if len(entries) == 0:
        return '\nNo Data'
    table = PrettyTable(headings)
    for heading in headings:
        table.align[heading] = 'l'
    for entry in entries:
        table.add_row(entry)
    if sortby:
        return table.get_string(sortby=sortby, reversesort=reversesort)
    else:
        return table.get_string()

def reachability_report(asns):
    headings = ['ANS', 'unique paths', 'Min', 'Max', 'Transit ASNs', 'Downstream ASNs']
    sortby   = 'Downstream ASNs'
    entries  = []
    entries = [[asn.id, len(asn.paths), min(map(len, asn.paths)), 
        max(map(len, asn.paths)), len(asn.transit_asns), len(asn.downstream_asns)] 
            for asn in asns]
    return report(headings, entries, sortby)

def main():
    args = get_args()
    set_log_level(args.verbose)
    cousteau_object = get_cousteau_object(args.msm_id)
    sagan_object    = get_sagan_objects(cousteau_object)
    asns            = Asns(sagan_object, args.pyasn_file)
    print reachability_report(asns.asns)
    print '{} ANS analysed'.format(len(asns))


if __name__ == '__main__':
    main()
