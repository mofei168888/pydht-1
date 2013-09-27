# K is closest good nodes
K = 8

# node id length
ID_BITS = 160

# Bootstrap nodes
BOOTSTRAP_NODES = [("router.utorrent.com", 6881, ""),
                   ("dht.transmissionbt.com", 6881, "")
                   ]

# dht config
DHT_ADDRESS= ("localhost", 6881)

# database config
DB_ADDRESS = "mongodb://localhost:27017/"
DB = "dhtdb"
ACTIVENODES = "activenodes"
