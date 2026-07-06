from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Resume Screening API"
    API_V1_STR: str = "/api/v1"
    
    # MySQL Database Connection String
    DATABASE_URL: str

    # Authentication
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days
    
    # Frontend URL for CORS
    FRONTEND_URL: str = "http://localhost:5174"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()
