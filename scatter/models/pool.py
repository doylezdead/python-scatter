import scatter.lib.hash_crypto as shashlib
import scatter.lib.networking as snetlib

class Member(object):
    id_hash = ""
    ip_addr = ""
    active = False
    
    def __init_(host=localhost, id_hash=None):
        if id_hash
        self.id_hash = shashlib.unique_hash()
        self.ip_addr = snetlib.host2ip(host)

class Pool(object):
    members = {}
    local_member = None

    def __init__():
        self.add_member()
    

    def add_member(host=None id_hash=None invoked_by=None):
        if host:
            remote_id = send add_member(id_hash=self.local_member.id_hash)
            

        elif id_hash or invoked_by:
            assert id_hash and invoked_by
            new_member = Member(host=invoked_by, id_hash=id_hash)
            self.members[new_member.id_hash] = new_member
            
            return self.local_member.id_hash to "invoked_by"

        else:
            new_member = Member()
            self.local_member = new_member
            


    def drop_member(hash_id):
        pass

    def announce_active(hash=None):
        if hash:
            self.members[hash].active = True
        else:
            for member in self.members
                snetlib.send_fn(member, 'announce_active', {'hash':self.local_member.id_hash})
