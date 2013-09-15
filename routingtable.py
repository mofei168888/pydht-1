import math
import bucket


class RoutingTable():
    def __init__(self):
        b = bucket.Bucket(0, 2 ** 160)
        self.nodes_dict = {}
        self.bucket = None
        self.buckets = {}
        self.nodes_by_addr = {}
        self.active_buckets = [b]

    def add_node(self, node):
        if node.node_id in self.nodes_dict:
            return True
        else:
            n = self.node_id_to_n(node.node_id)
            if n in self.buckets:
                self.bucket = self.buckets[n]
            else:
                self.bucket = self.buckets.keys[0]


    def node_id_to_n(self, node_id):
        node_id = long(str(node_id).encode("hex"), 16)
        return int(math.ceil(math.log(node_id, 2)))
