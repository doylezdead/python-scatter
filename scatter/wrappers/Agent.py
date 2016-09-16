from scatter.models.pool import Pool as ScatterPool
from scatter.lib.networking import send_fn
from multiprocessing import Process


class Agent(object):

    pool_proc = None
    local_member = None

    def __init__(self, target=None, ,hosts=None, port=15243):
        self.pool_proc = Process(target=ScatterPool, kwargs={'port':port})
        self.local_member = ('localhost', port)
        if type(hosts) in (list, set, tuple):
            for host in hosts:
                if type(host) in (list, tuple):
                    assert len(host) <= 2
                    assert type(host[0]) == str
                    if len(host) == 2:
                        assert type(host[1]) == int

                    self.add_member(host=host[0], port=host[1])

                elif type(host) == str:
                    self.add_member(host=host)

                else:
                    raise Exception('format')

    def add_member(self, **kwargs):
        send_fn(self.local_member, 'add_member', kwargs)

    def drop_member(self, **kwargs):
        send_fn(self.local_member, 'drop_member', kwargs)

    def get_members(self, **kwargs):
        send_fn(self.local_member, 'get_members', kwargs)

    def announce_active(self, **kwargs):
        send_fn(self.local_member, 'announce_active', kwargs)

    def announce_inactive(self, **kwargs):
        send_fn(self.local_member, 'announce_inactive', kwargs)

    def sync_quick(self, **kwargs):
        send_fn(self.local_member, 'sync_quick', kwargs)

    def sync_full(self, **kwargs):
        send_fn(self.local_member, 'sync_full', kwargs)