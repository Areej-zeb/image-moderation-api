import random
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Header
from datetime import datetime
from app.core.db import tokens_collection, usages_collection

moderation_router = APIRouter()

def verify_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    token = authorization.split(" ")[1]
    record = tokens_collection.find_one({"token": token})
    if not record:
        raise HTTPException(status_code=403, detail="Invalid token")
    return token

@moderation_router.post("/moderate")
async def moderate_image(token: str = Depends(verify_token), file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    # 🔍 MOCK moderation logic
    labels = ["violence", "nudity", "self-harm", "hate-symbols", "clean"]
    result = {
        "filename": file.filename,
        "content_type": file.content_type,
        "safe": True,
        "categories": []
    }

    # Simulate some random unsafe categories
    for label in labels[:-1]:  # skip "clean"
        if random.random() < 0.2:  # 20% chance
            result["safe"] = False
            result["categories"].append({
                "label": label,
                "confidence": round(random.uniform(0.7, 0.99), 2)
            })

    if result["safe"]:
        result["categories"].append({
            "label": "clean",
            "confidence": 1.0
        })

    # 📈 Log usage
    usages_collection.insert_one({
        "token": token,
        "endpoint": "/moderate",
        "timestamp": datetime.utcnow()
    })

    return result
