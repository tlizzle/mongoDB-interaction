from scripts.config import db, table, data_path, host
import logging
from pymongo import MongoClient
import pandas as pd

def insert_to_db():
    uri = f"mongodb://{host}:27017/test"

    client = MongoClient(uri)
    mydb = client[db]
    mydb = mydb[table]

    logging.info("Database and table created successfully")
    print(client.list_database_names())


    df = pd.read_csv(data_path + '/data.csv',
                    usecols= lambda x: x != 'Id')
    df['date'] = pd.to_datetime(df['date'])
    df['weekday'] = pd.to_datetime(df.date).dt.dayofweek.apply(lambda x: x+1).astype(str)

    data = df.to_dict('records')

    mydb.insert_many(data)
    logging.info("Records created successfully")


    # cursor = mydb.find({})
    # for document in cursor:
    #       print(document)

if __name__ == "__main__":
    insert_to_db()

