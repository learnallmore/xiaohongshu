from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "mysql+pymysql://root@127.0.0.1:3306/xiaohongshumoney"
    account_name: str = "棱镜"

    # 飞书提醒（GHA / 本机 feishu_remind）
    feishu_webhook_url: str = ""

    # 素材质量门槛
    material_min_likes: int = 800
    material_min_quality: int = 80


@lru_cache
def get_settings() -> Settings:
    return Settings()
