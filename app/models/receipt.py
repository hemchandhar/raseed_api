from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReceiptBase(BaseModel):
    file_name: str
    upload_date: datetime = datetime.now()
    user_id: str

class ReceiptInDB(ReceiptBase):
    id: str
