from datetime import datetime
from pydantic import BaseModel


class UsageOut(BaseModel):
    token: str
    endpoint: str
    timestamp: datetime
