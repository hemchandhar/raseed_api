from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_DETAILS: str = "mongodb://localhost:27017"
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    GOOGLE_CREDENTIALS_FILE: str = "google_credentials.json"

    class Config:
        env_file = ".env"

settings = Settings()
