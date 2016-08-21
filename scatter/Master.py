import socket as socket_lib

class Master(object):
    hosts = []
    def __init__(self, hosts=[]):
        self.hosts = hosts
        self.hosts = ['localhost']

    def start(self, verbose=False):
        for host in self.hosts:
            socket = socket_lib.socket()
            socket.connect((host,15243))
            socket.send("24")
            socket.close()

