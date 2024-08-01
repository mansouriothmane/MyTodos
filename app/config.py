from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOSTNAME: str

    JWT_SECRET: str
    JWT_ALGORITHM: str

    class ConfigDict:
        env_file = "./.env"


settings = Settings()
