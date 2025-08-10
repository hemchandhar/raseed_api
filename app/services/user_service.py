from ..core.database import user_collection
from ..models.user import UserCreate, UserInDB
from passlib.context import CryptContext
from jose import JWTError, jwt
from ..core.config import settings
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def create_user(user: UserCreate):
    user_dict = user.dict()
    if user.password:
        hashed_password = get_password_hash(user.password)
        user_dict.pop("password")
        user_dict["hashed_password"] = hashed_password
    result = await user_collection.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    return user_dict

async def get_user_by_email(email: str):
    user = await user_collection.find_one({"email": email})
    if user:
        user["id"] = str(user["_id"])
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
