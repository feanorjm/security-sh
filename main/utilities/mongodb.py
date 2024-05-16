from pymongo import MongoClient


def insert_data(event_obj):
    client = MongoClient("mongodb+srv://admin:$martHomy2022@cluster0.jntkxjs.mongodb.net/?retryWrites=true&w=majority")
    db = client.smarthomydb
    event = db.events
    res = event.insert_one(event_obj)
    return res
