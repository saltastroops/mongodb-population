import os
from pymongo import MongoClient

# mongodb connection
client = MongoClient(os.environ["MONGODB_URI"])
db = client.sdb2
proposals_collections = db.Proposals
blocks_collections = db.Blocks
blocks = db.Blocks