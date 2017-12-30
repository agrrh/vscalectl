import os
import sys

from lib.cache import Cache
from lib.api import API
from lib.client import Client


if __name__ == '__main__':
    try:
        token = os.environ['VSCALE_API_TOKEN']
    except KeyError:
        print('Please set "VSCALE_API_TOKEN" variable to be able to call API. Exiting.')
        sys.exit(1)

    cache = Cache('~/.vscalectl.yml', remove_cache=True)
    cache.load()

    api = API(token, cache)

    cli = Client(api, no_header=True)

    res = True

    res = res & bool(cli.do('images', None, None, {'image': None, 'plan': None, 'location': None}))
    print('Images: {}'.format(res))

    res = res & bool(cli.do('locations', None, None, {'image': None, 'plan': None, 'location': None}))
    print('Locations: {}'.format(res))

    res = res & bool(cli.do('plans', None, None, {'image': None, 'plan': None, 'location': None}))
    print('Plans: {}'.format(res))

    servers = cli.do('servers', None, None, {'image': None, 'plan': None, 'location': None})
    res = res & (True if servers is [] else bool(servers))
    print('Servers: {}'.format(res))

    if res:
        print('Passed.')
        sys.exit(0)
    else:
        print('Failed.')
        sys.exit(1)
