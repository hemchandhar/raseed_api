from pydantic import BaseModel
from datetime import datetime
from typing import List

class Transaction(BaseModel):
    id: str
    date: datetime
    amount: float
    description: str
    category: str

class UPITransactions(BaseModel):
    transactions: List[Transaction]
