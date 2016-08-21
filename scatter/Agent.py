from scatter.lib import *
import socket as socket_lib
import json

class Agent():
    target = None
    args = None
    port = None
    control = True
    job = None
    connection = None
    kwargs_dict = None

    def __init__(self, target=None, args={}, port=15243):
        self.target = target
        self.args = args
        self.port = port
    
    def start_job(self):
        self.target(**self.kwargs_dict)

    def kill_job(self):
        self.control = False # self-control lol
        self.connection.close()

    def status_job(self):
        pass

    def parse_control(self, control):
        actions = {"start": self.start_job,
                   "kill": self.kill_job,
                   "status": self.status_job}

        actions[control]()

    def listen(self, verbose=False):
        socket = socket_lib.socket()
        socket.bind(("0.0.0.0",self.port))
        socket.listen(1)  # first master to touch it wins

        while self.control:
            conn, address = socket.accept()
            self.connection = conn
            if verbose:
                print("master:{} connected".format(address))

            control_dict = recv_dict(conn)
            # print(control_dict)

            self.kwargs_dict = control_dict.get('kwargs',{})
            self.parse_control(control_dict['control'])
