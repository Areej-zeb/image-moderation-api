import os
import requests
import tempfile
from datetime import datetime, timezone
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Header

from app.core.db import tokens_collection, usages_collection
from dotenv import load_dotenv

load_dotenv()

moderation_router = APIRouter()

SIGHTENGINE_USER = os.getenv("SIGHTENGINE_USER")
SIGHTENGINE_SECRET = os.getenv("SIGHTENGINE_SECRET")

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

    # Save uploaded image temporarily
    temp_path = os.path.join(tempfile.gettempdir(), file.filename)
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    try:
        # Call Sightengine API
        url = "https://api.sightengine.com/1.0/check.json"
        params = {
            "models": "nudity,wad,gore",
            "api_user": SIGHTENGINE_USER,
            "api_secret": SIGHTENGINE_SECRET
        }

        with open(temp_path, "rb") as media_file:
            response = requests.post(url, data=params, files={"media": media_file})
            result = response.json()

        # Format results into categories array
        categories = []
        for label_group in ['nudity', 'gore', 'weapon', 'alcohol', 'drugs']:
            section = result.get(label_group)
            if isinstance(section, dict):
                for k, v in section.items():
                    categories.append({
                        "label": f"{label_group}:{k}",
                        "confidence": round(v, 2)
                    })
            elif isinstance(section, float):
                categories.append({
                    "label": label_group,
                    "confidence": round(section, 2)
                })

        # Safety logic
        nudity = result.get("nudity", {})
        safe_score = nudity.get("safe", 0)
        raw_score = nudity.get("raw", 0)
        partial_score = nudity.get("partial", 0)
        gore_score = result.get("gore", {}).get("prob", 0)
        weapon_score = result.get("weapon", 0)

        is_safe = (
            safe_score >= 0.9 and
            raw_score < 0.1 and
            partial_score < 0.1 and
            gore_score < 0.1 and
            weapon_score < 0.1
        )

        # Log usage
        usages_collection.insert_one({
            "token": token,
            "endpoint": "/moderate",
            "timestamp": datetime.now(timezone.utc)
        })

        return {
            "filename": file.filename,
            "safe": is_safe,
            "categories": categories
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass  # Prevent deletion failure from crashing the request
