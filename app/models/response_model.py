from pydantic import BaseModel
from typing import Any
class ResponseModel(BaseModel):
    status: str
    detail: Any