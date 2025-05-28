from pymongo import MongoClient
from datetime import datetime

from app.core.config import MONGO_URI
client = MongoClient(MONGO_URI)

db = client["moderation"]
tokens = db["tokens"]

tokens.delete_many({})  # Clear to avoid duplicates

admin_token = {
    "token": "128d8249e357b82f7e3e68ab65eca6c3",
    "isAdmin": True,
    "createdAt": datetime.utcnow()
}

tokens.insert_one(admin_token)
print("✅ Re-inserted admin token.")
