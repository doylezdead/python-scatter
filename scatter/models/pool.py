from scatter.lib import hash_crypto as shashlib
from scatter.lib import networking as snetlib
from scatter.models.member import Member


class Pool(object):
    members = {}
    # functions = {}
    local_member = None
    valid_pool = True

    def __init__(self):
        self.local_member = Member()
        # self.listen_loop()

    def _dummy(self):
        pass

    def listen_loop(self):
        socket = snetlib.get_listener_socket()
        while self.valid_pool:
            snetlib.listen(socket, self.distribute_job)
        socket.close()

    def distribute_job(self, control_dict):
        fn_name = control_dict.get('function','dummy')
        kwargs = control_dict.get('kwargs', {})

        requires_caller = (
            'add_member'
        )
        if fn_name not in requires_caller:
            del kwargs['invoked_by']
        
        fn_dict = {
            '_update_members': self._update_members,
            '_get_members': self._get_members,
            'sync_full': self.sync_full,
            'sync_quick': self.sync_quick,
            'add_member': self.add_member,
            'drop_member': self.drop_member,
            'announce_active': self.announce_active,
            'announce_inactive': self.announce_inactive,
            'dummy': self.announce_active
        }

        return fn_dict[fn_name](**kwargs)
    
    ### SYNCHRONIZE HOSTS ACROSS ALL MEMBERS' VERSIONS OF THE POOL
    def _update_members(self, full_map={}):
        for entry in full_map:
            if (entry in self.members.keys()) or (entry == self.local_member.id_hash):
                continue
            self.members[entry] = Member(bootstrap=full_map[entry])
    
    def _get_members(self):
        my_map = {}
        for id_hash in self.members:
            my_map[id_hash] = self.members[id_hash].to_dict()
        return my_map
    
    # this is a full sync.  Very expensive as it requires 2+ calls to each member from callee.
    def sync_full(self):
        full_map = self._get_members()
        
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
    def sync_quick(self):
        full_map = self._get_members()
        
        for id_hash in self.members:
            snetlib.send_fn(self.members[id_hash], '_update_members', full_map)
    
    ### MEMBER CONTROL
    # If the local member learns of/wishes to add a member, it is their duty
    # to add the host to their pool, add themselves to the host's pool, and full sync
    # to notify the rest of the pool of the new member's existence
    def add_member(self, host=None, id_hash=None, invoked_by=None):
        if host:
            # local add goes here
            remote_id = snetlib.send_fn(host, 'add_member', {'id_hash':self.local_member.id_hash})
            self.members[remote_id] = Member(host=host, id_hash=remote_id)
            return remote_id

        elif id_hash and invoked_by:
            # remote invoked add goes here
            new_member = Member(host=invoked_by, id_hash=id_hash)
            self.members[new_member.id_hash] = new_member
            return self.local_member.id_hash

        else:
            # (host) || (hash and invoker and !host)
            return "Failed."

    def drop_member(self, id_hash=None):
        return "https://youtu.be/jFi2ZM_7FnM?t=4m14s"
    
    ### SELF-ANNOUNCING FUNCTIONS. NOTIFY SOMETHING TO ENTIRE POOL ABOUT THIS MEMBER
    ## It will be the member's duty to mark itself offline if it cannot have any external
    ## function calls invoked on it
    def announce_inactive(self, id_hash=None):
        if id_hash:
            self.members[id_hash].active = False
            return "good"
        else:
            self.local_member.active = False
            for member in self.members:
                snetlib.send_fn(member, 'announce_active', {'hash':self.local_member.id_hash})
            return "good"
    
    def announce_active(self, id_hash=None):
        if id_hash:
            self.members[id_hash].active = True
            return "good"
        else:
            self.local_member.active = True
            for member in self.members:
                snetlib.send_fn(member, 'announce_active', {'hash':self.local_member.id_hash})
            return "good"
