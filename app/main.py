from fastapi import FastAPI
from .routers import auth, profile, receipts, transactions

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(profile.router, prefix="/profile", tags=["profile"])
app.include_router(receipts.router, prefix="/receipts", tags=["receipts"])
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])

@app.get("/")
async def root():
    return {"message": "Welcome to Raseed API"}
