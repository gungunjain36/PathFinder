from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Database settings
    POSTGRES_URL: str
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_ROLE_KEY: str
    
    # Twitter/X API Settings (TODO: Add these to .env when implementing X posting)
    # X_API_KEY: str
    # X_API_SECRET: str
    # X_ACCESS_TOKEN: str
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
