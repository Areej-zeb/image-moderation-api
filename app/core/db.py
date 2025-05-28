from pymongo import MongoClient
from app.core.config import MONGO_URI

client: MongoClient = MongoClient(MONGO_URI)
db = client["moderation"]

tokens_collection = db["tokens"]
usages_collection = db["usages"]
