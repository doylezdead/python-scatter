from scatter.lib import *
import socket as socket_lib

class Agent():
    target = None
    args = None
    port = None
    control = True
    job = None

    def __init__(self, target=None, args={}, port=15243):
        self.target = target
        self.args = args
        self.port = port
    
    def start_job(self):
        pass

    def kill_job(self):
        self.control = False # self-control lol

    def status_job(self):
        pass

    def listen(self, verbose=False):
        socket = socket_lib.socket()
        socket.bind(("0.0.0.0",self.port))
        socket.listen(1) # first master to touch it wins
        
        d_len = 0

        while self.control:
            conn, address = socket.accept()
            if verbose:
                print("master:{} connected".format(address))
            d_len = int(conn.recv(8))
            print(d_len)
            conn.close()
            
            conn, address = socket.accept()
            control_dict = json_to_dict(conn.recv(d_len))
            
            parse_control(control_dict['control'])

    def parse_control(self, control):
        actions = {"start": start_job,
                   "kill": kill_job,
                   "status": status_job}

        actions[control]()

        
