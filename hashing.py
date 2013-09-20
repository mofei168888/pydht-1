#! /usr/bin/env python3
#encoding:utf-8
import random
import hashlib
import binascii
import socket
from struct import unpack

import constants


def random_id(seed=None):
    if seed:
        random.seed(seed)
    return random.randint(0, (2 ** constants.ID_BITS) - 1)


def hash_function(data):
    return hashlib.sha1(str(data).encode()).digest()


def port_ntol(s):
    p = []
    q = []
    for i in s:
        b = bin(i).replace("0b", "")
        p.append(b)

    for i in p:
        while len(i) < 8:
            i = "0" + i
        q.append(i)

    s = "0b" + q[1] + q[0]

    return int(s, 2)


def split_nodes(nodes):
    nodes_list = []
    for i in range(0, 8):
        id = nodes[i*20:i*20+20]
        ip = nodes[i*20+20:i*20+24]
        port = nodes[i*20+24:i*20+26]

        ip = socket.inet_ntoa(bytes(ip.encode("latin-1")))
        port = port_ntol(port.encode("latin-1"))

        # print(i, binascii.hexlify(id.encode()), ip, port)
        nodes_list.append((ip, port, id))
    return nodes_list


if __name__ == "__main__":
    id = random_id()
    print(id)
    hashid = hash_function(id)
    print(hashid)
    print(len(hashid))
    print(split_nodes("dd"))
