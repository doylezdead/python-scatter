from scatter.lib import hash_crypto as shashlib
from scatter.lib import networking as snetlib
from scatter.models.member import Member

import logging
logging.basicConfig(level=logging.DEBUG)


class Pool(object):
    members = {}
    fn_dict = {}
    job_dict = {}
    local_member = None
    valid_pool = True

    def __init__(self, port=15243):
        self.local_member = Member(port=port)
        self.fn_dict = {
            '_update_members': self._update_members,
            'get_members': self.get_members,
            'sync_full': self.sync_full,
            'sync_quick': self.sync_quick,
            'add_member': self.add_member,
            'drop_member': self.drop_member,
            'announce_active': self.announce_active,
            'announce_inactive': self.announce_inactive,
            '_dummy': self._dummy
        }

    # Listener
    def listen(self):
        socket = snetlib.get_listener_socket(self.local_member.port)
        socket.listen(100)

        while self.valid_pool:
            snetlib.listen(socket, self.distribute_function)

        socket.close()

    def distribute_function(self, control_dict):
        fn_name = control_dict.get('function', '_dummy')
        kwargs = control_dict.get('kwargs', {})

        requires_caller = (
            'add_member'
        )
        if fn_name not in requires_caller:
            del kwargs['invoked_by']

        return self.fn_dict[fn_name](**kwargs)

    @staticmethod
    def _dummy():
        return "Failure"

    # SYNCHRONIZE HOSTS ACROSS ALL MEMBERS' VERSIONS OF THE POOL
    def _update_members(self, full_map=None):
        if not full_map:
            return 'Nothing to pass'
        for entry in full_map:
            if (entry in self.members.keys()) or (entry == self.local_member.id_hash):
                continue
            self.members[entry] = Member(bootstrap=full_map[entry])
        return 'Success'
    
    def get_members(self):
        my_map = {}
        for id_hash in self.members:
            my_map[id_hash] = self.members[id_hash].to_dict()
        return my_map
    
    # this is a full sync.  More expensive as it requires 2+ calls to each member from callee.
    def sync_full(self):
        full_map = self.get_members()
        
        for id_hash in self.members:
            full_map.update(snetlib.send_fn(self.members[id_hash], 'get_members', {}))

        self._update_members(full_map)

        for id_hash in self.members:
            snetlib.send_fn(self.members[id_hash], '_update_members', {'full_map': full_map})
    
    # this is a sync with reference to the callee.
    # Less expensive as it only requires 1 call to each member from callee.
    # references to members not known to the callee will not be destroyed on the callers
    #
    # useful for a system designed around an inactive member acting as a load-balancer.
    # if all members are added/dropped from master, you can just use quick sync
    def sync_quick(self):
        full_map = self.get_members()
        
        for id_hash in self.members:
            snetlib.send_fn(self.members[id_hash], '_update_members', {'full_map': full_map})
    
    ### MEMBER CONTROL
    # If the local member learns of/wishes to add a member, it is their duty
    # to add the host to their pool, add themselves to the host's pool, and full sync
    # to notify the rest of the pool of the new member's existence
    def add_member(self, host=None, port=15243, id_hash=None, invoked_by=None):
        if host:
            # local add goes here
            remote_id = snetlib.send_fn((host, port), 'add_member', {'port': self.local_member.port,
                                                                     'id_hash': self.local_member.id_hash})
            self.members[remote_id] = Member(host=host, id_hash=remote_id, port=port)
            return remote_id

        elif id_hash and invoked_by:
            # remote invoked add goes here
            new_member = Member(port=port, host=invoked_by, id_hash=id_hash)
            self.members[new_member.id_hash] = new_member
            return self.local_member.id_hash

        else:
            # (host) || (hash and invoker and !host)
            return "Failure"

    def drop_member(self, id_hash=None):
        return "https://youtu.be/jFi2ZM_7FnM?t=4m14s"
    
    # SELF-ANNOUNCING FUNCTIONS. NOTIFY SOMETHING TO ENTIRE POOL ABOUT THIS MEMBER
    # It will be the member's duty to mark itself offline if it cannot have any external
    # function calls invoked on it
    def announce_inactive(self, id_hash=None):
        if id_hash:
            # Remote call
            self.members[id_hash].active = False
            return "good"
        else:
            # Local call
            self.local_member.active = False
            for member in self.members:
                snetlib.send_fn(member, 'announce_inactive', {'id_hash': self.local_member.id_hash})
            return "good"
    
    def announce_active(self, id_hash=None):
        if id_hash:
            # Remote call
            self.members[id_hash].active = True
            return "good"
        else:
            # Local call announce self active and propogate to other members
            self.local_member.active = True
            for member in self.members:
                snetlib.send_fn(member, 'announce_active', {'id_hash':  self.local_member.id_hash})
            return "good"

    def job(self, target):
        self.job_dict[target.__name__] = target
        def reg():
            pass
        return reg
