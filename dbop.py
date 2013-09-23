#coding:utf-8
import threading
from pymongo import MongoClient

import constants


class DBOP():
    def __init__(self):
        self.lock = threading.Lock()
        self.client = MongoClient(constants.DB_ADDRESS)
        self.db = self.client[constants.DB]
        self.creat_index()
    
    def creat_index(self):
        self.db[constants.ACTIVENODES].ensure_index([("id", 1), ("unique", True)])
        
    def insert(self, t, s):
        table = self.db[t]
        return table.insert(s)
