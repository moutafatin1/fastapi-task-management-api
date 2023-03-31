from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URL: PostgresDsn
    SQLALCHEMY_DATABASE_URL_SYNC: PostgresDsn
    SITE_DOMAIN: str | None  # "site.com"

    class Config:
        env_file = ".env"


settings = Settings()  # type: ignore
