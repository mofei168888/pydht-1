class Bucket(object):
    def __init__(self, range_min, range_max, maxsize=8):
        self._nodes = set()

        self.range_min = range_min
        self.range_max = range_max
        self.maxsize = maxsize

    def add_node(self, node):
        if not self.key_in_range(node.node_id):
            return False

        if node in self._nodes:
            return True

        if self.full():
            return False

        self._nodes.add(node)

        return True

    def remove_node(self, node):
        if node in self._nodes:
            self._nodes.remove(node)
            return True

        return False

    def key_in_range(self, key):
        return self.range_min <= key < self.range_max

    def full(self):
        return len(self._nodes) == self.maxsize
