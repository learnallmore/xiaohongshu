from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "mysql+pymysql://root@127.0.0.1:3306/xiaohongshumoney"
    account_name: str = "棱镜编辑部"


@lru_cache
def get_settings() -> Settings:
    return Settings()
