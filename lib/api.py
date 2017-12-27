import requests
import sys


class API(object):
    def __init__(self, token, cache):
        self.addr = 'https://api.vscale.io/v1/'
        self.token = token
        self.cache = cache

        self.cache.location = self._closest_location() or self.cache.location
        self.cache.plan = self.cache.plan or 'small'
        self.cache.image = self.cache.image or self._best_image()
        self.cache.keys = self.cache.keys or [
            k['id'] for k in self.call('sshkeys')
        ]

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
            res = methods_map[method](self.addr + path, headers=headers, json=data).json()
        except:
            print("Error occured: {}".format(sys.exc_info()[0]))
            res = False

        return res

    def _best_image(self):
        images_all = self.call('images')

        # Narrow by location, plan, purpose and then os type and version
        images_select = [i for i in images_all if self.cache.location in i['locations']]
        images_select = [i for i in images_select if i['active']]
        images_select = [i for i in images_select if self.cache.plan in i['rplans']]
        images_select = [i for i in images_select if 'master' in i['id']]
        images_select = [i for i in images_select if 'ubuntu' in i['id']]

        # Trying to find latest LTS version
        try:
            images_select = [i for i in images_select if '.04' in i['id'] and int(i['id'][7:9]) % 2 == 0]
        except:
            images_select = [i for i in images_select if '.04' in i['id']]

        # Make list of IDs
        images_select = [i['id'] for i in images_select]
        images_select.sort(reverse=True)

        return images_select[0]

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

    servers_one_get = servers_one

    def servers_one_create(self, name, image=None, plan=None, location=None, keys=None):
        data = {
            'make_from': self.image_default if image is None else image,
            'rplan': self.plan_default if plan is None else plan,
            'do_start': True,
            'name': name,
            'hostname': name,
            'keys': self.keys_default if keys is None else keys,
            'location': self.location_default if location is None else location
        }
        return self.call('scalets/', method='POST', data=data)
