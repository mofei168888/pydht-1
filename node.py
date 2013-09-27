import b


class Node(object):
    def __init__(self, host, port, id):
        self.host = host
        self.port = port
        self.id = id

    def address(self):
        return (self.host, self.port)

    def distance(self, id):
        return self.id ^ id

    def _sendmessage(self, message, sock=None, address=None, lock=None):
        message = b.bencode(message)
        # print(address)
        # print(message)
        if sock:
            sock.sendto(bytes(message.encode()), address)

    def ping(self, sock=None, node_id=None, lokc=None):
        message = {}

    def find_node(self, id, sock=None, node=None, lock=None):
        message = {"t": "aa", "y": "q", "q": "find_node"}
        messagea = {}
#         messagea["id"] = str(self.id.decode("latin"))
#         messagea["target"] = str(self.id.decode("latin"))
        messagea["id"] = str(self.id, "latin-1")
        messagea["target"] = str(id, "latin-1")
        message["a"] = messagea
        if node:
            address = node.address()
            self._sendmessage(message, sock, address, lock)

if __name__ == "__main__":
    node = Node(1000, ("192.168.1.0", 6881))
    d = node.distance(30)
    print(d)
