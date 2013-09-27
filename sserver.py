import socketserver
import threading
import time
import b
import node
import math
import logging
import hashing
import constants
import dbop


FORMAT = "%(asctime)-15s %(levelname)s %(lineno)d %(funcName)s %(thread)d " + \
           "%(message)s"
logging.basicConfig(filename="log.txt",
                    filemode="w",
                    format=FORMAT)
logger = logging.getLogger("sserver")

logger.setLevel(logging.INFO)
logger.debug("debug start -------------------------------------")

class DHTUDPRequestHandler(socketserver.DatagramRequestHandler):

    def handle(self):
        odata = self.request[0].strip()
        data = odata.decode("latin-1")
        # sock = self.request[1]
        client_address = self.client_address
        print("connecting:", client_address)
        logger.debug("connecting: %s", client_address)
        if not data:
            return None
        else:
            self.server.dht.findlist.activelist_append(client_address)
            
        # print("activelist length:", len(self.server.dht.findlist.activelist))
        # print("activelist:", self.server.dht.findlist.activelist)
        try:
            message = b.bdecode(data)
        except:
            print("b.bdeconde error")
            return None
        if message is None:
            print(odata)
            return None

        if message['y'] == 'q':
            logger.info("q: %s %s", client_address, message["q"])
            id = message["r"]["id"]
            n = node.Node(client_address[0], client_address[1], id)
            self.handle_query(n, message)
            
        elif message["y"] == "r":
            id = message["r"]["id"]
            n = node.Node(client_address[0], client_address[1], id)
            try:
                self.server.dht.db_op.insert("activenodes", 
                                             {"host": n.host, 
                                              "port": n.port, 
                                              "id": n.id})
            except:
                pass
            self.handle_response(n, message)
            
        elif message["y"] == "e":
            print("kprc error:", message["e"])
        

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
            # print("r_find_nodes")
            nodes = message["r"]["nodes"]
            nodes = hashing.split_nodes(nodes)
          
            self.server.dht.findlist.extend(nodes)
        
        
class DHTUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


class DHT(object):
    def __init__(self, host, port, id=None):
        if not id:
            id = hashing.random_id()
            
        id = hashing.hash_function(id)
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
        n = ()
        try:  
            n = self.findlist.list.pop()
        except:
            # print("start: ------------------------------------------------------")
            self.findlist.extend(constants.BOOTSTRAP_NODES)
            n = self.findlist.list.pop()
            
        t = threading.Timer(1, self.sched_find, (n, ))
        t.start()
            
    
    def sched_find(self, n):
        boot_node = node.Node(n[0], n[1], 0)
        self.iteractive_find_node(boot_node)
        time.sleep(5)
        self.bootstrap()


    def iteractive_find_node(self, boot_node=None):
        self.node.find_node(self.node.id, self.server.socket, boot_node)


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
    count = 100
    ids = hashing.create_ids(count)
    ports = [p for p in range(6800, 6800+count)]
    address = list(zip(ids, ports))

    for id, port in address:
        HOST, PORT = "", port
        d = threading.Timer(2, DHT, (HOST, PORT, id))
        d.start()
