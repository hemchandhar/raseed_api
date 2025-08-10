from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from ..services import user_service
from ..models.user import UserCreate, UserPublic, Token
from datetime import timedelta
from ..core.config import settings
import google.oauth2.credentials
import google_auth_oauthlib.flow


router = APIRouter()

@router.post("/register", response_model=UserPublic)
async def register(user: UserCreate):
    db_user = await user_service.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    created_user = await user_service.create_user(user=user)
    return UserPublic(**created_user)

@router.post("/login/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await user_service.get_user_by_email(email=form_data.username)
    if not user or not user_service.verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = user_service.create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/login/google")
async def login_google():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        settings.GOOGLE_CREDENTIALS_FILE,
        scopes=["https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile", "openid"],
        redirect_uri="http://localhost:8000/auth/google"
    )
    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true"
    )
    return RedirectResponse(authorization_url)

@router.get("/auth/google")
async def auth_google(request: Request):
    state = request.query_params.get("state")
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        settings.GOOGLE_CREDENTIALS_FILE,
        scopes=["https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile", "openid"],
        state=state,
        redirect_uri="http://localhost:8000/auth/google"
    )
    authorization_response = str(request.url)
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    user_info = credentials.id_token

    user = await user_service.get_user_by_email(email=user_info["email"])
    if not user:
        user = await user_service.create_user(UserCreate(email=user_info["email"], password="", full_name=user_info["name"]))

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = user_service.create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
