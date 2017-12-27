import os
import yaml
import time


class Cache(object):
    def __init__(self, path, dont_use_cache, expiration=1209600):
        self.file_path = os.path.expanduser(path)
        self.file_expiration = expiration

        self.image = None
        self.keys = None
        self.location = None
        self.plan = None

        if dont_use_cache:
            try:
                os.remove(path)
            except FileNotFoundError:
                pass

    def load(self):
        data = None
        if os.path.exists(self.file_path) and os.path.getmtime(self.file_path) > time.time() - self.file_expiration:
            with open(self.file_path, 'r') as fp:
                data = yaml.load(fp)
            fp.close()
        res = bool(data)

        if data:
            try:
                self.image = data['image']
                self.keys = data['keys']
                self.location = data['location']
                self.plan = data['plan']
            except:
                res = False

        return res

    def save(self):
        data = {
            'image': self.image,
            'keys': self.keys,
            'location': self.location,
            'plan': self.plan
        }
        with open(self.file_path, 'w+') as fp:
            fp.write(yaml.dump(data))
        fp.close()

        return True
