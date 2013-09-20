import socketserver
import threading
import b
import node
import math
import binascii
import hashing
import constants


class DHTUDPRequestHandler(socketserver.DatagramRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        data = data.decode("latin-1")
        # sock = self.request[1]
        client_address = self.client_address
        print(client_address)

        if not data:
            return None

        try:
            message = b.bdecode(data)
        except:
            print("error")
            return None

        print(message)
        id = message["r"]["id"]
        n = node.Node(client_address[0], client_address[1], id)

        if message['y'] == 'q':
            self.handle_query(n, message)
        elif message["y"] == "r":
            self.handle_response(n, message)
        

    def handle_query(self, node, message):
        if message['q'] == 'ping':
            print("ping:" + message['a']['id'])
            print(math.log(str(message['a']['id'])))
        elif message['q'] == 'find_node':
            print("find_node:" + message['a']['target'])
        elif message['q'] == 'get_peers':
            print("get_peers:" + message['info_hash'])
        elif message['q'] == 'announce_peer':
            print("announce_peer:" + message['port'])

    def handle_response(self, node, message):
        if "nodes" in message["r"]:
            print("r_find_nodes")
            nodes = message["r"]["nodes"]
            nodes = hashing.split_nodes(nodes)
            print(nodes)
        


class DHTUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


class DHT(object):
    def __init__(self, host, port, id=None):
        if not id:
            id = hashing.random_id()
            id = hashing.hash_function(id)
        self.node = node.Node(host, port, id)
        self.data = {}

        self.server = DHTUDPServer((HOST, PORT), DHTUDPRequestHandler)
        self.server.dht = self
        self.bootstrap(constants.BOOTSTRAP_NODES[0][0],
                       constants.BOOTSTRAP_NODES[0][1])
        self.server_thread = threading.Thread(
            target=self.server.serve_forever())
        self.server_thread.daemon = True
        self.server_thread.start()

    def bootstrap(self, boot_host, boot_port):
        if boot_host and boot_port:
            boot_node = node.Node(boot_host, boot_port, 0)
            self.iteractive_find_node(boot_node)

    def iteractive_find_node(self, boot_node=None):
        if boot_node:
            self.node.find_node(id, self.server.socket, boot_node)


if __name__ == "__main__":
    HOST, PORT = "", 6881
    DHT(HOST, PORT)
