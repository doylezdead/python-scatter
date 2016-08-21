from scatter.lib import *
import socket as socket_lib
from multiprocessing import Process
import time

a = Process()


class Agent(object):
    target = None
    port = None

    control = True
    args_set = None
    kwargs_dict = None
    pool_id = -1
    master_hostname = ""

    def __init__(self, target=None, port=15243):
        self.target = target
        self.port = port

    def start_job(self):
        return self.target(*self.args_set, **self.kwargs_dict)

    def stop_agent(self):
        self.control = False  # self-control lol

    def status_job(self):
        pass

    def parse_control(self, control):
        actions = {"start": self.start_job,
                   "stop": self.stop_agent,
                   "status": self.status_job}

        return actions[control]()

    def listen(self, verbose=False):
        socket = socket_lib.socket()
        socket.setsockopt(socket_lib.SOL_SOCKET, socket_lib.SO_REUSEADDR, 1)

        socket.bind(("0.0.0.0", self.port))
        socket.listen(1)  # first master to touch it wins

        while self.control:
            if verbose:
                print("Waiting on job from master")

            conn, address = socket.accept()
            self.master_hostname = address[0]

            if verbose:
                print("master:{} connected".format(self.master_hostname))

            control_dict = recv_dict(conn)

            self.kwargs_dict = control_dict.get('kwargs', {})
            self.args_set = set(control_dict.get('args', []))

            self.pool_id = control_dict.get('pool_id',-1)
            send_reply(conn, "Success from id: {}".format(str(self.pool_id).zfill(2)))
            conn.close()

            retval = self.parse_control(control_dict['control'])

            if not self.control:
                break


            # now that the return value is ready, send it back
            failcount = 0
            while failcount < 12:
                try:
                    return_socket = socket_lib.socket()
                    return_socket.connect((self.master_hostname, self.port+1))

                    send_dict(return_socket, {"pool_id": self.pool_id, "retval": retval})
                    return_socket.close()
                    break

                except ConnectionRefusedError:
                    failcount += 1
                    time.sleep(.25)

        socket.close()
