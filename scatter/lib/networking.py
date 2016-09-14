import json
import socket


def host2ip(hostname):
    return socket.gethostbyname(hostname)


def get_listener_socket(port=51423):
    # socket setup
    new_socket = socket.socket()
    new_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    new_socket.bind(("0.0.0.0", port))

    return new_socket


def _send_dict(conn, input_dict):
    str_input_dict = json.dumps(input_dict)
    conn.send((str(len(str_input_dict)).zfill(16)).encode('utf-8'))
    conn.recv(1)
    conn.send(str_input_dict.encode('utf-8'))


def _recv_dict(conn):
    d_len = int(conn.recv(16).decode('utf-8'))
    conn.send("1".encode('utf-8'))
    return json.loads(conn.recv(d_len).decode('utf-8'))


def listen(new_socket, callback):
    new_socket.listen(1)
    conn, invoker = new_socket.accept()  # Note, This is blocking

    control_dict = _recv_dict(conn)
    control_dict['invoked_by'] = invoker

    retval = callback(control_dict)
    _send_dict(new_socket, {'return': retval})
    conn.close()


def send_fn(member, function_name, kwargs, port=51423):
    hostname = member.__str__()

    new_socket = socket.socket()
    new_socket.connect((hostname, port))
    control_dict = {
        'function': function_name,
        'kwargs': kwargs
    }
    _send_dict(new_socket, control_dict)
    retval = _recv_dict(new_socket)['return']
    new_socket.close()
    return retval


def send_str(conn, in_str):
    conn.send(in_str.encode('utf-8'))


def get_str(conn):
    return conn.recv(19).decode('utf-8')

