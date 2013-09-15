
class Node(object):
    def __init__(self, address):
        self.node_id = ''
        self.address = address

    def distance(self, node_id):
        return self.node_id ^ node_id

    def _sendmessage(self, message, sock=None, node_id=None, lock=None):
        if sock:
            sock.sendto(message, node_id.address)

    def ping(self, sock=None, node_id=None, lokc=None):
        message = {}


if __name__ == "__main__":
    node = Node(1000, ("192.168.1.0", 6881))
    d = node.distance(30)
    print d
