from pymongo import MongoClient
import pymongo
import json
from datetime import datetime
from bson import BSON
from bson import json_util
import re
from bson.objectid import ObjectId
import pandas as pd
from scripts.config import host




class MongoConnection(object):    
    def __init__(self, host= host, port=27017, db_name='test'):
        """
        在開啟認證模式之後，如果將用戶密碼寫入 url 中，默認連接的資料庫是 admin。但其實連接的資料庫並不是 admin，所以使用者名稱和密碼是無效的，所以導致認證失敗
        解決方式：在 url 中指定所要連接的資料庫，或是在選擇資料庫之後 （ db = client['log_fieldmap ']  ）
        """
        # uri = f"mongodb://{username}:{password}@{host}:{port}/{db_name}?authMechanism=SCRAM-SHA-1"
        uri = f"mongodb://{host}:{port}"

        self.client = MongoClient(uri) #making a connection with MongoClient
        self.db = self.client[db_name] #getting a Database
        #a single instance of mongoDB can support multi independent db

    def change_db(self, db_name=""):
        self.db = self.client[db_name] 

    def close(self):
        self.client.close()
         
         #adding indexes can help sccelerate certain queries
    def ensure_index(self, table_name, index=None):
        self.db[table_name].ensure_index([(index, pymongo.GEOSPHERE)])

    def create_table(self, table_name, index=None):
        self.db[table_name].create_index([(index, pymongo.DESCENDING)])

    def get_one(self, table_name, conditions={}, showfield = {}):
        single_doc = self.db[table_name].find_one(conditions, showfield and showfield or None)
        return single_doc

    def get_all(self, table_name, conditions={}, showfield = {}, sort_index='_id', limit=0):
        all_doc = self.db[table_name].find(conditions, showfield and showfield or None).sort(sort_index, pymongo.DESCENDING).limit(limit)
        return all_doc

    def insert_one(self, table_name, value):
        self.db[table_name].insert_one(value)
        #insert a new dict

    def insert_many(self, table_name, value):
        self.db[table_name].insert_many(value)
        #insert many new dicts

    def delete_one(self, table_name, value):
        self.db[table_name].remove(value)

    def update_push(self, table_name, where, what):
        # print where, what
        self.db[table_name].update(where, {"$push": what}, upsert=False)

    def update(self, table_name, where, what):
        # print where, what
        self.db[table_name].update(where, {"$set": what}, upsert=False)

    def update_multi(self, table_name, where, what):
        self.db[table_name].update(where, {"$set": what},upsert=False, multi=True)

    def update_upsert(self, table_name, where, what):
        self.db[table_name].update(where, {"$set": what},upsert=True)

    def map_reduce(self, table_name, mapper, reducer, query, result_table_name):
        myresult = self.db[table_name].map_reduce(mapper, reducer, result_table_name, query)
        return myresult
        #http://www.runoob.com/mongodb/mongodb-map-reduce.html 

    def map_reduce_search(self, table_name, mapper, reducer, query, sort_by, sort = -1, limit = 20):
        if sort_by == "distance":
            sort_direction = pymongo.ASCENDING
        else:
            sort_direction = pymongo.DESCENDING
        myresult = self.db[table_name].map_reduce(mapper, reducer,'results', query)
        results = self.db['results'].find().sort("value."+sort_by, sort_direction).limit(limit)
        return results

    def aggregate_all(self, table_name, conditions={}): #主要用于处理数据(诸如统计平均值,求和等)，并返回计算后的数据结果。有点类似sql语句中的 count(*)。
        all_doc = self.db[table_name].aggregate(conditions)
        return all_doc

    def group(self, table_name, key, condition, initial, reducer):
        all_doc = self.db[table_name].group(key=key, condition=condition, initial=initial, reduce=reducer)
        return all_doc

    def get_count(self, table_name, conditions={}, sort_index='_id'):
        count = self.db[table_name].find(conditions).count()
        return count

if __name__ == "__main__":
    conn = MongoConnection()

 




