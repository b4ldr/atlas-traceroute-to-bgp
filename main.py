#!/usr/bin/env python

import logging
from argparse import ArgumentParser
from typing import Any, Optional

from prettytable import PrettyTable

from trace2bgp.atlas import Asns
from trace2bgp.utils import get_cousteau_object, get_sagan_objects


def get_args():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('--pyasn-file')
    parser.add_argument('msm_id')
    return parser.parse_args()

def get_log_level(args_level: int) -> int:  # pragma: no cover
    """Convert an integer to a logging log level.

      Arguments:
          args_level (int): The log level as an integer

      Returns:
          int: the logging loglevel
    """
    return {
            0: logging.ERROR,
            1: logging.WARN,
            2: logging.INFO,
            3: logging.DEBUG,
            }.get(args_level, logging.DEBUG)

def set_log_level(args_level: int):
    """Set the log level for the application.

      Arguments:
          args_level (int): The log level as an integer
    """
    log_level = get_log_level(args_level)
    lib_log_level = get_log_level(args_level if args_level == 0 else args_level - 1)
    logging.basicConfig(level=log_level)
    logging.getLogger('requests').setLevel(lib_log_level)
    logging.getLogger('urllib3').setLevel(lib_log_level)

def report(headings: list[str], entries: list[list[Any]], sortby: Optional[str] = None, reversesort: bool = False) -> str:
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

def reachability_report(asns: Asns) -> str:
    headings = ['ANS', 'unique paths', 'Min', 'Max', 'Transit ASNs', 'Downstream ASNs']
    sortby   = 'Downstream ASNs'
    entries  = []
    entries = [[asn.id, len(asn.paths), min(map(len, asn.paths)),
        max(map(len, asn.paths)), len(asn.transit_asns), len(asn.downstream_asns)]
            for asn in asns.asns]
    return report(headings, entries, sortby)

def main():
    args = get_args()
    set_log_level(args.verbose)
    cousteau_object = get_cousteau_object(args.msm_id)
    if not cousteau_object:
        return 1
    sagan_object    = get_sagan_objects(cousteau_object)
    asns            = Asns(sagan_object, args.pyasn_file)
    print(reachability_report(asns))
    print(f'{len(asns)} ANS analysed')


if __name__ == '__main__':
    main()
