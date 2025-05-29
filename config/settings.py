from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BASE_URL: str = "https://pos.test.dadus.cwcloud.in/pos"
    DEFAULT_TIMEOUT: int = 30000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"