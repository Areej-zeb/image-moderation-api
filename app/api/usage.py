from fastapi import APIRouter, Header, HTTPException, Depends
from app.core.db import usages_collection, tokens_collection
from app.models.usage import UsageOut

usage_router = APIRouter()

def verify_admin_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    token = authorization.split(" ")[1]
    record = tokens_collection.find_one({"token": token})
    if not record or not record.get("isAdmin", False):
        raise HTTPException(status_code=403, detail="Admin token required")
    return token

@usage_router.get("/usage", response_model=list[UsageOut])
def get_usage(_=Depends(verify_admin_token)):
    usage_docs = usages_collection.find({}, {"_id": 0}).sort("timestamp", -1)
    return list(usage_docs)
