from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')
db = client.sdb2
proposals_collections = db.Proposals
blocks_collections = db.Blocks
blocks = db.Blocks