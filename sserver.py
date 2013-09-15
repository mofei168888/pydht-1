import socketserver
import threading
import bencode
import node
import math


class ThreadedUDPRequestHandler(socketserver.DatagramRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        client_address = self.client_address
        print(client_address)

        if not data:
            return None

        try:
            message = bencode.bdecode(data)
        except:
            print("error")
            return None

        print(message)

        n = node.Node(client_address)

        if message['y'] == 'q':
            self.handle_query(n, message)
        else:
            self.handle_response(n, message)

        cur_thread = threading.current_thread()
        response = "{}:{}".format(cur_thread.name, data)
        socket.sendto(response, self.client_address)

    def handle_query(self, node, message):
        if message['q'] == 'ping':
            print("ping:" + message['a']['id'])
            print(math.log(long(str(message['a']['id']).encode("hex"), 16), 2))
        elif message['q'] == 'find_node':
            print("find_node:" + message['a']['target'])
        elif message['q'] == 'get_peers':
            print("get_peers:" + message['info_hash'])
        elif message['q'] == 'announce_peer':
            print("announce_peer:" + message['port'])

    def handle_response(self, node, message):
        return None


class ThreadUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = "", 6881

    server = ThreadUDPServer((HOST, PORT), ThreadedUDPRequestHandler)
    ip, port = server.server_address

    print(ip, port)

    server_thread = threading.Thread(target=server.serve_forever())

    server_thread.daemon = True
    server_thread.start()

    print("server loop running in thread:", server_thread.name)
    #server.serve_forever()
