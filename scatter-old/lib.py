import json


def send_dict(conn, input_dict):
    str_input_dict = json.dumps(input_dict)
    conn.send(str(len(str_input_dict.encode('utf-8'))).encode('utf-8'))
    conn.recv(1)
    conn.send(str_input_dict.encode('utf-8'))


def recv_dict(conn):
    d_len = int(conn.recv(8).decode('utf-8'))
    conn.send("1".encode('utf-8'))
    return json.loads(conn.recv(d_len).decode('utf-8'))


def send_reply(conn, in_str):
    conn.send(in_str.encode('utf-8'))


def get_reply(conn):
    return conn.recv(19).decode('utf-8')
