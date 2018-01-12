import requests
import sys


class API(object):
    def __init__(self, token, cache):
        self.addr = 'https://api.vscale.io/v1/'
        self.token = token
        self.cache = cache

        self.cache.location = self._closest_location() or self.cache.location or 'spb0'
        self.cache.plan = self.cache.plan or 'small'
        self.cache.image = self.cache.image or self._best_image() or 'ubuntu_16.04_64_001_master'
        self.cache.keys = self.cache.keys or [k['id'] for k in self.call('sshkeys')]

        self.cache.save()

    def call(self, path, method='GET', data=None):
        methods_map = {
            'GET': requests.get,
            'PUT': requests.put,
            'POST': requests.post,
            'PATCH': requests.patch,
            'DELETE': requests.delete,
        }

        headers = {'X-Token': self.token}

        try:
            response = methods_map[method](self.addr + path, headers=headers, json=data)
            result = response.json()
        except:
            print("Error occured: {}".format(sys.exc_info()[0]))
            result = False

        if result is False:
            print('Could not call API or parse output, exiting. Response:')
            print(data)
            print(response)
            sys.exit(1)

        return result

    def _best_image(self):
        images_all = self.call('images')

        # Narrow by location, plan, purpose and then os type and version
        images_select = list(filter(lambda i: i['active'], images_all))
        images_select = list(filter(lambda i: 'ubuntu' in i['id'], images_select))
        images_select = list(filter(lambda i: 'master' in i['id'], images_select))

        images_select = list(filter(lambda i: self.cache.location in i['locations'], images_select))
        images_select = list(filter(lambda i: self.cache.plan in i['rplans'], images_select))

        # Trying to find latest LTS version by seeking for xx.04 where xx is even number
        try:
            images_select = list(filter(
                lambda i: '.04' in i['id'] and int(i['id'][7:9]) % 2 == 0,
                images_select
            ))
        except:
            images_select = list(filter(
                lambda i: '.04' in i['id'],
                images_select
            ))

        # Make list of IDs
        images_select = [i['id'] for i in images_select]

        try:
            res = images_select[-1]
        except IndexError:
            res = None

        return res

    def _closest_location(self):
        """Try to get user's geolocation and calculate closest which of data-centers is closest. Fallback to msk0 when errors occur."""
        try:
            from haversine import haversine
            user_geo = requests.get('http://freegeoip.net/json/').json()
        except:
            print("Warning, haversine could not detect geo info: {}".format(sys.exc_info()[0]))
            user_geo = False

        if user_geo \
            and isinstance(user_geo['latitude'], float) \
            and user_geo['latitude'] > 0 \
            and isinstance(user_geo['longitude'], float) \
            and user_geo['longitude'] > 0:

            available_locations = {
                'msk0': (55.4521, 37.3704),
                'spb0': (59.5700, 30.1900)
            }

            user = (user_geo['latitude'], user_geo['longitude'])

            # Earth circumference / 2 to represent maximum value possible
            # (2 * pi * 6371) / 2
            min_distance = 20015.08
            for loc in available_locations:
                distance = haversine(user, available_locations[loc])
                if distance < min_distance:
                    min_distance = distance
                    res = loc
        else:
            res = 'msk0'
        return res

    def account(self):
        return self.call('account')

    def images(self):
        return self.call('images')

    def locations(self):
        return self.call('locations')

    def plans(self):
        return self.call('rplans')

    def servers_list(self):
        return self.call('scalets')

    def servers_one(self, ctid):
        return self.call('scalets/' + str(ctid))
