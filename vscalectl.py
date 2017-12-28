#!/usr/bin/env python3

import sys
import os
import argparse

from lib.cache import Cache
from lib.api import API
from lib.client import Client


epilog = """usage:

  vscalectl account                  Display account info.
            locations                Show available data-centers.
            images                   List OS repository.
            plans                    Inspect resources and prices.

            servers                  Show all servers.
            servers <ID>             Get single server information.
            servers <Name> create    Create new server with specific name and hostname.
            servers <ID> stop        Stop (shutdown) server.
            servers <ID> start       Turn server on.
            servers <ID> restart     Reboot server.
            servers <ID> rebuild     Reinstall server from original image.
            servers <ID> delete      Permanently remove server.

  Please visit control panel on https://vscale.io/panel/ to perform more complex actions.
"""

def args_parse(epilog):
    parser = argparse.ArgumentParser(
        description='CLI tool to operate vscale.io API.',
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        'object', metavar='OBJECT', type=str,
        help='Type of target object: account, servers, etc.'
    )
    parser.add_argument(
        'identifier', metavar='IDENTIFIER', type=str, nargs='?',
        help='Identifier of an object, e.g. server ID.'
    )
    parser.add_argument(
        'action', metavar='ACTION', type=str, nargs='?',
        help='Action to perform, e.g. start/stop.'
    )

    parser.add_argument('--no-header', action='store_true', help='Do not print header in lists.')

    parser.add_argument('--cache-file', type=str, default='~/.vscalectl.yml', help='Path of file to store cached default parameters.')
    parser.add_argument('--no-cache', action='store_true', help='Remove cache file before running script.')

    return parser, parser.parse_args()

if __name__ == '__main__':
    token = os.environ['VSCALE_API_TOKEN'] if 'VSCALE_API_TOKEN' in os.environ else False

    if not token:
        print('Please set "VSCALE_API_TOKEN" variable to be able to call API. Exiting.')
        sys.exit(1)

    parser, args = args_parse(epilog)

    cache = Cache(args.cache_file, dont_use_cache=args.no_cache)
    cache.load()

    api = API(token, cache)

    cli = Client(api, no_header=args.no_header)
    if not cli.do(args):
        parser.print_help()
        sys.exit(0)
