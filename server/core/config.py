from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_HOST: str
    API_PORT: int
    PEERS_DB_URL: str
    DISCOVERY_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
