from scatter.lib import *
import socket as socket_lib
import json

class Master(object):
    hosts = []
    kwargs = {}
    def __init__(self, hosts=[], kwargs={}):
        self.kwargs = kwargs
        self.hosts = hosts
        self.hosts = ['localhost']

    def start(self, verbose=False):
        for host in self.hosts:
            socket = socket_lib.socket()
            socket.connect((host,15243))

            control_dict = {'control': 'start', 'kwargs': self.kwargs}

            send_dict(socket, control_dict)

            socket.close()

