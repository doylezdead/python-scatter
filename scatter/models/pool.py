import scatter.lib.hash_crypto as shashlib
import scatter.lib.networking as snetlib
from scatter.models.member import Member


class Pool(object):
    members = {}
    # functions = {}
    local_member = None
    valid_pool = True

    def __init__():
        self.add_member()
        self.net_listen()

    def net_listen():
        while self.valid_pool:
            snetlib.listen(self.distribute_job)

    def distribute_job(function="" kwargs={}, invoked_by=None)
        requires_caller = (
            'add_member'
        )
        if function in requires_caller:
            kwargs['invoked_by'] = invoked_by

        self.__dict__[function](**kwargs)
    
    ### SYNCHRONIZE HOSTS ACROSS ALL MEMBERS' VERSIONS OF THE POOL
    def _update_members(full_map={}):
        for entry in full_map:
            if ((entry in self.members.keys()) or (entry == self.local_member.id_hash)):
                continue
            self.members[entry] = Member(bootstrap=full_map[entry])
    
    def _get_members():
        my_map = {}
        for id_hash in self.members:
            my_map[id_hash] = self.members[id_hash].to_dict()
        return my_map
    
    # this is a full sync.  Very expensive as it requires 2+ calls to each member from callee.
    def sync_full()
        full_map = _get_members()
        
        for id_hash in self.members:
            full_map.update(snetlib.send_fn(self.members[id_hash],'_get_members',{}))

        self._update_members(full_map)

        for id_hash in self.members:
            snetlib.send_fn(self.members[id_hash], '_update_members', full_map)
    
    # this is a sync with reference to the callee.
    # Less expensive as it only requires 1 call to each member from callee.
    # references to members not known to the callee will not be destroyed on the callers
    #
    # useful for a system designed around an inactive member acting as a load-balancer.
    # if all members are added/dropped from master, you can just use quick sync
    def sync_quick()
        full_map = _get_members()
        
        for id_hash in self.members:
            snetlib.send_fn(self.members[id_hash], '_update_members', full_map)
    
    ### MEMBER CONTROL
    def add_member(host=None id_hash=None invoked_by=None):
        if host:
            remote_id = send add_member(id_hash=self.local_member.id_hash)

        elif id_hash and invoked_by:
            assert id_hash and invoked_by
            new_member = Member(host=invoked_by, id_hash=id_hash)
            self.members[new_member.id_hash] = new_member
            return self.local_member.id_hash to "invoked_by"

        else:
            new_member = Member()
            self.local_member = new_member

    def drop_member(id_hash=None):
        pass
    
    ### SELF-ANNOUNCING FUNCTIONS. NOTIFY SOMETHING TO ENTIRE POOL ABOUT THIS MEMBER
    ## It will be the member's duty to mark itself offline if it cannot have any external
    ## function calls invoked on it
    def announce_inactive(id_hash=None):
        if id_hash:
            self.members[id_hash].active = False
        else:
            self.local_member.active = False
            for member in self.members:
                snetlib.send_fn(member, 'announce_active', {'hash':self.local_member.id_hash})
    
    def announce_active(id_hash=None):
        if id_hash:
            self.members[id_hash].active = True
        else:
            self.local_member.active = True
            for member in self.members:
                snetlib.send_fn(member, 'announce_active', {'hash':self.local_member.id_hash})
