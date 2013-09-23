#coding:utf-8
import socketserver
import threading
import time
import sched
import sqlite3
import b
import node
import math
import binascii
import hashing
import constants
import dbop


s = sched.scheduler(time.time,time.sleep)

class DHTUDPRequestHandler(socketserver.DatagramRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        data = data.decode("latin-1")
        # sock = self.request[1]
        client_address = self.client_address
        print("connecting:", client_address)
        print("re:", data)

        if not data:
            return None
        else:
            self.server.dht.findlist.activelist_append(client_address)
            
        print("activelist length:", len(self.server.dht.findlist.activelist))
        print("activelist:", self.server.dht.findlist.activelist)
        try:
            message = b.bdecode(data)
        except:
            print("error")
            return None

        # print(message)
        id = message["r"]["id"]
        n = node.Node(client_address[0], client_address[1], id)
        
        self.server.dht.db_op.insert("activenodes", {"host": n.host, "port": n.port, "id": n.id})
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
            
            self.server.dht.findlist.extend(nodes)
            print(len(self.server.dht.findlist.list))
            print(self.server.dht.findlist.list)
        


class DHTUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


class DHT(object):
    def __init__(self, host, port, id=None):
        if not id:
            id = hashing.random_id()
            id = hashing.hash_function("3")
        self.node = node.Node(host, port, id)
        self.data = {}
        self.join_nodes = constants.BOOTSTRAP_NODES
        self.findlist = Findlist()
        self.server = DHTUDPServer((host, port), DHTUDPRequestHandler)
        self.server.dht = self
        self.db_op = dbop.DBOP()
        self.bootstrap()
        self.server_thread = threading.Thread(
            target=self.server.serve_forever())
        self.server_thread.daemon = True
        self.server_thread.start()
           
    def bootstrap(self):
        l = len(self.findlist.list)
        print("lenght:", l)
        n = ()
        try:  
            n = self.findlist.list.pop()
        except:
            print("start: ------------------------------------------------------")

            self.findlist.extend(constants.BOOTSTRAP_NODES)
            print(self.findlist.list)
            n = self.findlist.list.pop()
            
        t = threading.Timer(1, self.sched_find, (n, ))
        t.start()
            

            

    
    def sched_find(self, n):
        boot_node = node.Node(n[0], n[1], 0)
        self.iteractive_find_node(boot_node)
        time.sleep(5)
        self.bootstrap()


    def iteractive_find_node(self, boot_node=None):
        self.node.find_node(id, self.server.socket, boot_node)


class Findlist(object):
    def  __init__(self):
        self.list = []
        self.activelist = []
        self.lock = threading.Lock()
    
    def extend(self, l):
        with self.lock:
            self.list.extend(l)
            return self.list
    
    def activelist_append(self, l):
        with self.lock:
            if l not in self.activelist:
                self.activelist.append(l)
            return self.activelist
            

if __name__ == "__main__":
    HOST, PORT = "", 6881
    DHT(HOST, PORT)
