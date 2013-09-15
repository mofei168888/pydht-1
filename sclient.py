#! /usr/bin/env python3
import socket
import hashlib
import b
import binascii


def get_node_id(id):
    m = hashlib.sha1()
    m.update(id.encode('utf-8'))
    return m.digest()


def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.sendto(bytes(message.encode('utf-8')), (ip, port))
        data, server = sock.recvfrom(1024)
        data = data.decode("latin-1")
        print("Received: {}".format(data))

        datadict = b.bdecode(str(data))
        print(datadict)
        s = datadict["r"]["id"]
        print(s)
        print(s.encode("utf-8"))
        print(binascii.hexlify(s.encode("utf-8")))
    except socket.error:
        sock.close()
    finally:
        sock.close()


if __name__ == "__main__":
    message = "d1:ad2:id20:" + "abcdefghij0123456789" +\
              "e1:q4:ping1:t2:aa1:y1:qe"

    # client("127.0.0.1", 6881, "H1")
    client("router.bittorrent.com", 6881, message)
