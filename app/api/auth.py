import secrets
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Header, Body, Path
from fastapi.responses import JSONResponse
from app.core.db import tokens_collection
from app.models.token import TokenOut, TokenCreateRequest

auth_router = APIRouter()

# Admin token verification
def verify_admin_token(authorization: str = Header(..., alias="Authorization")):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    token = authorization.split(" ")[1]
    record = tokens_collection.find_one({"token": token})
    if not record or not record.get("isAdmin", False):
        raise HTTPException(status_code=403, detail="Admin token required")

    return record

# POST /auth/tokens
@auth_router.post("/auth/tokens", response_model=TokenOut)
def create_token(
    data: TokenCreateRequest = Body(...),
    _=Depends(verify_admin_token)
):
    token = secrets.token_hex(16)
    token_data = {
        "token": token,
        "isAdmin": data.is_admin,
        "createdAt": datetime.utcnow()
    }
    tokens_collection.insert_one(token_data)
    return token_data

# GET /auth/tokens
@auth_router.get("/auth/tokens")
def list_tokens(_=Depends(verify_admin_token)):
    tokens = tokens_collection.find()
    output = []
    for token in tokens:
        token.pop("_id", None)
        if isinstance(token.get("createdAt"), datetime):
            token["createdAt"] = token["createdAt"].isoformat()
        output.append(token)
    return output

# DELETE /auth/tokens/{token}
@auth_router.delete("/auth/tokens/{token}", response_class=JSONResponse)
def delete_token(
    token: str = Path(..., description="The token string to delete"),
    _=Depends(verify_admin_token)
):
    result = tokens_collection.delete_one({"token": token})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Token not found")
    return {"message": "Token deleted"}
