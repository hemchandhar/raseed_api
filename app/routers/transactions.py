from fastapi import APIRouter, Depends
from ..services import transaction_service
from ..models.transaction import UPITransactions
from .profile import get_current_user
from ..models.user import UserPublic

router = APIRouter()

@router.get("/upi", response_model=UPITransactions)
async def get_upi_transactions(current_user: UserPublic = Depends(get_current_user)):
    return await transaction_service.get_upi_transactions(current_user["_id"])
