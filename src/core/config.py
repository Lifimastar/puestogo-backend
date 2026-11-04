from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    database_url: str = Field(..., env="DATABASE_URL")

    class Config:
        env_file = ".env"
        # Evita que la clave se muestre en los logs de FastAPI
        hide_input_in_errors = True

settings = Settings()