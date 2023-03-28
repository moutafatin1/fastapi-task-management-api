from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URL: PostgresDsn

    class Config:
        env_file = ".env"


settings = Settings()  # type: ignore
