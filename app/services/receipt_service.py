from ..core.database import receipt_collection
from ..models.receipt import ReceiptBase
from bson import ObjectId

async def create_receipt(receipt: ReceiptBase):
    receipt_dict = receipt.dict()
    result = await receipt_collection.insert_one(receipt_dict)
    return {**receipt_dict, "_id": result.inserted_id}

async def get_receipts_by_user_id(user_id: str):
    return await receipt_collection.find({"user_id": user_id}).to_list(100)
