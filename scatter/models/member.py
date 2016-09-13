import scatter.lib.hash_crypto as shashlib
import scatter.lib.networking as snetlib

class Member(object):
    id_hash = ""
    ip_addr = ""
    active = False
    consec_failures = 0 # used by scatter networking functions to determine
                        # the member's effectiveness in the pool
    
    def __init_(host=localhost, id_hash=None, bootstrap=None):
        if bootstrap:
            self.__dict__.update(bootstrap)
            return

        if id_hash:
            self.id_hash = id_hash
        else:
            self.id_hash = shashlib.unique_hash()
        self.ip_addr = snetlib.host2ip(host)

    def to_dict():
        return {
            'id_hash': self.id_hash,
            'ip_addr': self.ip_addr,
            'active': self.active
        }