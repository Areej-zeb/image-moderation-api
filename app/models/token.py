from datetime import datetime
from pydantic import BaseModel


class TokenCreateRequest(BaseModel):
    is_admin: bool


class TokenOut(BaseModel):
    token: str
    isAdmin: bool
    createdAt: datetime
