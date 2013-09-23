from pymongo import MongoClient


client = MongoClient("localhost", 27017)

db = client["dht-database"]

dbactivelist = db["activelist"]
activelist_id = dbactivelist.insert({"host": "192.1368.120.12"})
print(activelist_id)
