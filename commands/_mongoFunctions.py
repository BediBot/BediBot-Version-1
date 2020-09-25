import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["bedibot"]

mycol = db["guilds"]

print(db.list_collection_names())