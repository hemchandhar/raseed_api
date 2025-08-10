from fastapi import APIRouter, Depends, UploadFile, File
from ..services import receipt_service
from ..models.receipt import ReceiptBase, ReceiptInDB
from .profile import get_current_user
from ..models.user import UserPublic
from typing import List

router = APIRouter()

@router.post("/upload", response_model=ReceiptInDB)
async def upload_receipt(file: UploadFile = File(...), current_user: UserPublic = Depends(get_current_user)):
    # In a real application, you would save the file to a cloud storage like S3
    # and store the file path in the database.
    receipt = ReceiptBase(file_name=file.filename, user_id=current_user["_id"])
    created_receipt = await receipt_service.create_receipt(receipt)
    return created_receipt

@router.get("/", response_model=List[ReceiptInDB])
async def get_receipts(current_user: UserPublic = Depends(get_current_user)):
    return await receipt_service.get_receipts_by_user_id(current_user["_id"])
