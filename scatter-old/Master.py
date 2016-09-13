from scatter.lib import *
import socket as socket_lib
import time


class Master(object):
    kwargs = {}
    args = ()
    connections = {}
    port = 0

    def __init__(self, hosts=[], args=(), kwargs={}, port=15243):
        self.kwargs = kwargs
        self.args = args
        self.port = port

        index = 0
        for host in hosts:
            self.connections[host] = index
            index += 1

    def _send_start(self, host):
        failcount = 0
        while failcount < 12:
            try:
                control_dict = {'pool_id': self.connections[host],
                                'control': 'start',
                                'args': list(self.args),
                                'kwargs': self.kwargs}

                socket = socket_lib.socket()
                socket.connect((host, 15243))

                send_dict(socket, control_dict)
                reply = get_reply(socket)

                socket.close()
                break

            except ConnectionRefusedError:
                failcount += 1
                time.sleep(.25)

    def start_one(self, host, verbose=False):
        self._send_start(host)

    def stop(self):
        for host in self.connections:
            socket = socket_lib.socket()
            socket.connect((host, 15243))
            send_dict(socket, {'control': 'stop'})
            socket.close()

    def start(self, verbose=False):
        # Distribute jobs to agents
        for host in self.connections:
            self._send_start(host)

        # Await responses from all agents
        print("waiting for returns")

        return_socket = socket_lib.socket()
        return_socket.setsockopt(socket_lib.SOL_SOCKET, socket_lib.SO_REUSEADDR, 1)
        return_socket.bind(("0.0.0.0", self.port+1))
        return_socket.listen(len(self.connections))

        reply_count = 0
        while reply_count < len(self.connections):
            conn, address = return_socket.accept()
            retdict = recv_dict(conn)
            conn.close()
            reply_count += 1
            print("==== agent:{} return value ====\n{}\n".format(retdict['pool_id'], retdict['retval']))

        return_socket.close()
