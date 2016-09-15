from scatter.lib import hash_crypto as shashlib
import scatter.lib.networking as snetlib


class Member(object):
    id_hash = ""
    ip_addr = ""
    active = False
    port = -1
    consec_failures = 0  # used by scatter networking functions to determine
                         # the member's effectiveness in the pool
    
    def __init__(self, port=0, host='localhost', id_hash=None, bootstrap=None):
        if bootstrap:
            self.__dict__.update(bootstrap)
            return

        if id_hash:
            self.id_hash = id_hash
        else:
            self.id_hash = shashlib.unique_hash()
        self.ip_addr = snetlib.host2ip(host)
        self.port = port

    def to_dict(self):
        return {
            'id_hash': self.id_hash,
            'active': self.active,
            'ip_addr': self.ip_addr,
            'port': self.port
        }

    def __str__(self):
        return "{}:{}".format(self.ip_addr, self.port)


