from scripts.mongo import MongoConnection
from scripts.config import db, table, host
import pandas as pd
from datetime import datetime
from bson.objectid import ObjectId


def get_data1():
    conn = MongoConnection(host= host, port=27017, db_name= db)
    start = datetime(2014, 7, 9)
    end = datetime(2014, 7, 10)

    result = conn.get_all(table_name= table, conditions= {'date':{ "$gte" : start, "$lt" : end}}, limit=10)
    data = []
    for r in result:
        data.append(r)

    return pd.DataFrame(data)

def get_data2():
    conn = MongoConnection(host= host, port=27017, db_name= db)
    df = list(conn.get_all(table_name= table, conditions={'country': 'USA', "_id": ObjectId("62c1375c510e55995e0db401")}))

    # final = pd.concat([result1,result2], ignore_index = True, axis = 0)
    # with pd.ExcelWriter('output.xlsx', options={'strings_to_urls': False}) as writer:
    #     # dateframe 寫入
    #     final.to_excel(writer, sheet_name='Sheet_name_1')

    return pd.DataFrame(df)


def get_aggregate_data():
    conn = MongoConnection(host= host, port=27017, db_name= db)

    result = conn.aggregate_all(table_name= table, conditions=(
    [{
    "$group" : 
        {"_id" : "$city", 
         "country" : {"$sum" : 1}
         }}
    ]))

    return pd.DataFrame(result)