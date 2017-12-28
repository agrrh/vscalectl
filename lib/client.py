import netaddr
from lib.templates import Templates


class Client(object):
    def __init__(self, api, no_header=False):
        self.api = api
        self.templates = Templates()

        self.no_header = no_header

    def account(self, identifier, action):
        data = self.api.call('account')

        status = 'OK' if data['status'] == 'ok' and not data['info']['is_blocked'] else 'Inactive or blocked!'
        name = ' '.join(filter(None, (
            data['info']['name'], data['info']['middlename'], data['info']['surname'])
        ))

        print(self.templates.ACCOUNT.format(
            id=data['info']['id'],
            status=status,
            name=name,
            email=data['info']['email'],
            phone=data['info']['mobile']
        ))

    def servers(self, identifier, action):
        if identifier:
            if action == 'get':
                data = self.api.call('scalets/{}'.format(identifier))
            elif action == 'create':
                data = self.api.call('scalets'.format(identifier), method='POST', data={
                    'make_from': self.api.cache.image,
                    'rplan': self.api.cache.plan,
                    'do_start': True,
                    'name': identifier,
                    'hostname': identifier,
                    'keys': self.api.cache.keys,
                    'location': self.api.cache.location
                })
            elif action == 'stop':
                data = self.api.call('scalets/{}/stop'.format(identifier), method='PATCH')
            elif action == 'start':
                data = self.api.call('scalets/{}/start'.format(identifier), method='PATCH')
            elif action == 'restart':
                data = self.api.call('scalets/{}/restart'.format(identifier), method='PATCH')
            elif action == 'rebuild':
                data = self.api.call('scalets/{}/rebuild'.format(identifier), method='PATCH')
            elif action == 'delete':
                data = self.api.call('scalets/{}'.format(identifier), method='DELETE')
            else:  # Fallback to get
                data = self.api.call('scalets/{}'.format(identifier))

            res = self.templates.SERVERS_ONE.format(
                ctid=data['ctid'],
                name=data['name'],
                hostname=data['hostname'],
                status=data['status'],
                image=data['made_from'],
                plan=data['rplan'],
                locked='yes' if data['locked'] else 'no',
                keys=', '.join(['{id}:{name}'.format(**key) for key in data['keys']]),
                location=data['location'],
                address='{ip} @ {gateway}/{mask}'.format(
                    ip=data['public_address']['address'],
                    gateway=data['public_address']['gateway'],
                    mask=netaddr.IPAddress(data['public_address']['netmask']).netmask_bits(),
                ) if data['public_address'] else '0.0.0.0 @ 0.0.0.0/0',
                address_private=' {ip} @ {gateway}/{mask}'.format(
                    ip=data['private_address']['address'],
                    gateway=data['private_address']['gateway'],
                    mask=netaddr.IPAddress(data['private_address']['netmask']).netmask_bits()
                ) if data['private_address'] else ''
            )
        else:
            data = self.api.call('scalets')
            res = []
            if not self.no_header:
                res.append(self.templates.SERVERS_ROW.format(
                    ctid='CTID',
                    name='Name',
                    status='Status',
                    image='Image',
                    plan='Plan',
                    location='Loc',
                    locked='',
                    address='Address'
                ))
            for server in data:
                res.append(self.templates.SERVERS_ROW.format(
                    ctid=server['ctid'],
                    name=server['name'] if len(server['name']) < 24 else server['name'][:22] + "…",
                    status=server['status'],
                    image=server['made_from'],
                    plan=server['rplan'],
                    locked='L ' if server['locked'] else '',
                    location=server['location'],
                    address=server['public_address']['address']
                ))

        if isinstance(res, (list)):
            print("\n".join(res))
        else:
            print(res)

    def images(self, identifier, action):
        data = self.api.call('images')

        # Optimize locations field
        data_optimized = {}
        for image in data:
            if image['id'] not in data_optimized and image['active']:
                data_optimized[image['id']] = image
            else:
                if image['description'] == data_optimized[image['id']]['description'] \
                    and image['rplans'] == data_optimized[image['id']]['rplans']:
                    data_optimized[image['id']]['locations'] += image['locations']
        data = [data_optimized[i] for i in data_optimized]

        res = []
        for image in data:
            res.append(self.templates.IMAGES_ROW.format(
                id=image['id'],
                description=image['description'],
                plans=','.join(sorted(image['rplans'])),
                locations=','.join(sorted(image['locations']))
            ))
        res.sort(key=lambda x: x[0])  # Sort list of images by ID
        if not self.no_header:
            res.insert(0, self.templates.IMAGES_ROW.format(
                id='ID',
                description='Description',
                size='Size',
                active='Active',
                plans='Plans',
                locations='Locations'
            ))
        print("\n".join(res))

    def locations(self, identifier, action):
        data = self.api.call('locations')

        res = []
        if not self.no_header:
            res.append(self.templates.LOCATIONS_ROW.format(
                id='ID',
                description='Description',
                plans='Plans'
            ))
        for loc in data:
            res.append(self.templates.LOCATIONS_ROW.format(
                id=loc['id'],
                description=loc['description'],
                plans=','.join(sorted(loc['rplans']))
            ))
        print("\n".join(res))

    def plans(self, identifier, action):
        data = self.api.call('rplans')
        data_prices = self.api.call('billing/prices')['default']

        res = []
        if not self.no_header:
            res.append(self.templates.PLANS_ROW.format(
                id='ID',
                price='Price',
                cpus='CPU',
                ram='RAM',
                disk='Disk',
                ips='IPs',
                locations='Locations'
            ))
        for plan in data:
            res.append(self.templates.PLANS_ROW.format(
                id=plan['id'],
                price=[int(data_prices[p]['month']/100) for p in data_prices if p == plan['id']][0],
                cpus=plan['cpus'],
                ram=str(round(plan['memory'] / 1024, 1)) + 'G',
                disk=str(int(plan['disk'] / 1024)) + 'G',
                ips=plan['addresses'],
                locations=','.join(sorted(plan['locations']))
            ))
        print("\n".join(res))

    def do(self, args):
        objects_map = {
            'account': self.account,

            'servers': self.servers,

            'images': self.images,
            'locations': self.locations,
            'plans': self.plans
        }

        if args.object in objects_map:
            objects_map[args.object](args.identifier, args.action)
            return True

        return False
