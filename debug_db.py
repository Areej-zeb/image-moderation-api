from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["moderation"]
tokens = db["tokens"]

all_tokens = list(tokens.find())

print("\n--- All Tokens in DB ---")
for token in all_tokens:
    print(token)