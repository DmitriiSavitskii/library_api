from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
