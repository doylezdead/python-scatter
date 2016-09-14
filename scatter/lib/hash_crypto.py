import hashlib
# import pycrypto
import time
import os

def ip_hash(ip):
    new_hash = hashlib.sha1()
    new_hash.update(ip.encode('utf-8'))
    return new_hash.hexdigest()

def unique_hash():
    new_hash = hashlib.sha1()
    new_hash.update(str(os.urandom(64)).encode('utf-8'))
    return new_hash.hexdigest()

