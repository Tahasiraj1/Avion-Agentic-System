from pydantic import BaseModel
from typing import Optional

class UpdateOrder(BaseModel):
    order_id: str
    quantity: Optional[int] = None
    size: Optional[str] = None
    color: Optional[str] = None
