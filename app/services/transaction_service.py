from ..models.transaction import Transaction, UPITransactions
from datetime import datetime

async def get_upi_transactions(user_id: str) -> UPITransactions:
    # This is a mock service. In a real application, you would integrate with a financial data provider.
    transactions = [
        Transaction(id="1", date=datetime.now(), amount=100.0, description="Coffee", category="Food"),
        Transaction(id="2", date=datetime.now(), amount=500.0, description="Movie", category="Entertainment"),
        Transaction(id="3", date=datetime.now(), amount=2000.0, description="Groceries", category="Food"),
    ]
    return UPITransactions(transactions=transactions)
